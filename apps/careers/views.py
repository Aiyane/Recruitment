from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication

from .serializer import ActivitySerializer, ImageSerializer
from .dal import ActivityDAL
from .service import ActivityService
from utils.viewsets import ModelViewSet, WriteOnlyModelViewSet
from utils.decorator import Validation


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

    @Validation.need_permission(error_msg="无权限创建活动！")
    def perform_create(self, serializer):
        """
        创建活动
        :param serializer: 创建活动的参数
        :return: 
        """
        identity = self.request.user.identity
        activity = serializer.validated_data['classification']
        serializer.validated_data['user'] = self.request.user
        return ActivityService.create_activity(identity, activity, **serializer.validated_data)


class ImageViewset(WriteOnlyModelViewSet):
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_adapter = {'all': ImageSerializer}
    no_login_methods = ()

    @Validation.not_return_false("没有创建权限！")
    def perform_create(self, serializer):
        """
        创建图片
        :param serializer: 创建图片的参数
        :return: 
        """
        serializer.validated_data['user'] = self.request.user
        activity_id = serializer.validated_data['activity']
        activity = ActivityDAL.get_activity_by_id(activity_id)
        serializer.validated_data['activity'] = activity
        if ActivityService.is_user_activity(self.request.user, activity):
            return serializer.save()
        return False
