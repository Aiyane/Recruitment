from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework import serializers

from .serializer import ActivitySerializer, ImageSerializer
from utils.viewsets import ModelViewSet, WriteOnlyModelViewSet
from .dal import ActivityDAL
from .service import DynamicService


class ActivityViewset(ModelViewSet):
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    no_login_methods = ('retrieve', 'list')
    serializer_adapter = {'all': ActivitySerializer}

    def make_queryset(self):
        user = self.request.user
        self.update_queryset('list', ActivityDAL.get_activity_by_field)
        self.update_queryset('retrieve', ActivityDAL.get_activity_by_field)
        self.update_queryset('update', ActivityDAL.get_activity_by_field, user=user)
        self.update_queryset('partial_update', ActivityDAL.get_activity_by_field, user=user)
        self.update_queryset('destroy', ActivityDAL.get_activity_by_field, user=user)

    def perform_create(self, serializer):
        identity = self.request.user.identity
        activity = serializer.validated_data['classification']
        serializer.validated_data['user'] = self.request.user
        instance, msg = DynamicService.create_dynamic(identity, activity, **serializer.validated_data)
        if not instance:
            raise serializers.ValidationError(msg)
        return instance


class ImageViewset(WriteOnlyModelViewSet):
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_adapter = {'all': ImageSerializer}
    no_login_methods = ()

    def perform_create(self, serializer):
        serializer.validated_data['user'] = self.request.user
        num = serializer.validated_data['activity']
        serializer.validated_data['activity'] = ActivityDAL.get_activity_by_id(num)
        return serializer.save()
