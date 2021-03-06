from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from utils import mixins


class ViewSet:
    @property
    def _serializer_adapter(self):
        """
        viewset 需要有 seriallizer_adapter 属性
        :return: 
        """
        if hasattr(self, 'serializer_adapter'):
            return getattr(self, 'serializer_adapter')
        raise NotImplementedError('`serializer_adapter` attribute does not exist.')

    @property
    def _no_login_methods(self):
        """
        viewset 需要有 no_login_methods 属性
        :return: 
        """
        if hasattr(self, 'no_login_methods'):
            return getattr(self, 'no_login_methods')
        raise NotImplementedError('`no_login_methods` attribute does not exist.')

    @property
    def _action(self):
        if hasattr(self, 'action'):
            return getattr(self, 'action')
        raise NotImplementedError('`%r` must inherit utils.GenericViewSet.' % self.__class__)

    @property
    def _queryset_map(self):
        if hasattr(self, 'queryset_map'):
            return getattr(self, 'queryset_map')
        raise NotImplementedError('`%r` must inherit utils.GenericViewSet.' % self.__class__)

    def make_queryset(self):
        """
        viewset 需要重载 make_queryset 方法
        :return: 
        """
        raise NotImplementedError('`make_queryset()` must be implemented.')

    def get_serializer_class(self):
        if self._action in self._serializer_adapter:
            return self._serializer_adapter[self._action]
        if 'all' in self._serializer_adapter:
            return self._serializer_adapter['all']
        if 'other' in self._serializer_adapter:
            return self._serializer_adapter['other']
        raise AttributeError('`serializer_adapter` not has the `%r` key' % self._action)

    def get_permissions(self):
        return [] if self._action in self._no_login_methods else [IsAuthenticated()]

    def update_queryset(self, method, func, **kwargs):
        """
        为请求方法提供查询方法
        :param method: 方法
        :param func: 查询方法
        :param kwargs: 查询条件
        :return: 
        """
        self._queryset_map[method] = func(**kwargs)

    def get_queryset(self):
        self.make_queryset()
        return self._queryset_map[self._action]


class GenericViewSet(ViewSet, viewsets.GenericViewSet):
    def __init__(self, **kwargs):
        self.queryset_map = {}
        super(GenericViewSet, self).__init__(**kwargs)


class ModelViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    """
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.
    """
    pass


class ReadOnlyModelViewSet(mixins.RetrieveModelMixin,
                           mixins.ListModelMixin,
                           GenericViewSet):
    """
    A viewset that provides default `list()` and `retrieve()` actions.
    """
    pass


class WriteOnlyModelViewSet(mixins.UpdateModelMixin,
                            mixins.CreateModelMixin,
                            GenericViewSet):
    """
    A viewset that provides default `list()` and `retrieve()` actions.
    """
    pass


class NoDestroyModelMixin(mixins.CreateModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.UpdateModelMixin,
                          mixins.ListModelMixin,
                          GenericViewSet):
    """
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()` and `list()` actions.
    """
    pass


class CreateDestroyModelMixin(mixins.CreateModelMixin,
                              mixins.DestroyModelMixin,
                              GenericViewSet):
    """
    A viewset that provides default `create()`, `destroy()` actions.
    """


class CreateListDestroyModelMixin(mixins.CreateModelMixin,
                                  mixins.ListModelMixin,
                                  mixins.DestroyModelMixin,
                                  GenericViewSet):
    """
    A viewset that provides default `create()`, `destroy()` and `list()` actions.
    """