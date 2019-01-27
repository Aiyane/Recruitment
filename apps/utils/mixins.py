from rest_framework.response import Response
from rest_framework import status
from rest_framework.settings import api_settings
from .service import BaseService


class MixinAbstract:
    def _get_func_or_raise_error(self, func_name):
        if hasattr(self, func_name):
            return getattr(self, func_name)
        raise NotImplementedError('`%r` must inherit utils.GenericViewSet.' % self.__class__)

    @property
    def _get_serializer(self):
        return self._get_func_or_raise_error('get_serializer')

    @property
    def _filter_queryset(self):
        return self._get_func_or_raise_error('filter_queryset')

    @property
    def _get_queryset(self):
        return self._get_func_or_raise_error('get_queryset')

    @property
    def _get_object(self):
        return self._get_func_or_raise_error('get_object')

    @property
    def _paginate_queryset(self):
        return self._get_func_or_raise_error('paginate_queryset')

    @property
    def _get_paginated_response(self):
        return self._get_func_or_raise_error('get_paginated_response')

    @property
    def _service_class(self):
        return getattr(self, 'service_class', BaseService)

    def service_drive(self, action, request, instance_or_queryset):
        return getattr(self._service_class, action)(request, instance_or_queryset)


class CreateModelMixin(MixinAbstract):
    """
    Create a model instance.
    """
    def create(self, request):
        serializer = self._get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        self.service_drive('create', request, instance)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


class ListModelMixin(MixinAbstract):
    """
    List a queryset.
    """
    def list(self, request, *args, **kwargs):
        queryset = self._filter_queryset(self._get_queryset())
        queryset = self.service_drive('list', request, queryset)
        page = self._paginate_queryset(queryset)
        if page is not None:
            serializer = self._get_serializer(page, many=True)
            return self._get_paginated_response(serializer.data)

        serializer = self._get_serializer(queryset, many=True)
        return Response(serializer.data)


class RetrieveModelMixin(MixinAbstract):
    """
    Retrieve a model instance.
    """
    def retrieve(self, *args, **kwargs):
        instance = self._get_object()
        serializer = self._get_serializer(instance)
        return Response(serializer.data)


class UpdateModelMixin(MixinAbstract):
    """
    Update a model instance.
    """
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self._get_object()
        serializer = self._get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_update(serializer)
        if kwargs.get('partial'):
            self.service_drive('update', request, instance)
        else:
            self.service_drive('partial_update', request, instance)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        return serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class DestroyModelMixin(MixinAbstract):
    """
    Destroy a model instance.
    """
    def destroy(self, request, *args, **kwargs):
        instance = self._get_object()
        instance = self.service_drive('destroy', request, instance)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()
