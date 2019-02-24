from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication

from .serializer import (ActivitySerializer, ImageSerializer, LikeSerializer, CollectSerializer,
                         GroupSerializer, UserGroupRefSerializer)
from .dal import ActivityDAL, LikeDAL, CollectDAL, UserGroupRefDAL, GroupDAL
from .service import ActivityService, ImageService
from utils.viewsets import ModelViewSet, WriteOnlyModelViewSet, CreateDestroyModelMixin, CreateListDestroyModelMixin
from utils.decorator import Validation


class ActivityViewset(ModelViewSet):
    """
    list:
        不需要登录，获取所有活动
    create:
        登录用户创建活动
    update:
        登录用户修改活动
    partial_update:
        登录用户修改活动
    destroy:
        登录用户删除活动
    retrieve:
        不需要登录，获取某个活动详情
    """
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
    """
    create:
        登录用户为相关活动上传相关图片
    update:
        登录用户修改相关活动上传相关图片
    partial_update:
        登录用户修改相关活动上传相关图片
    """
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_adapter = {'all': ImageSerializer}
    no_login_methods = ()

    def perform_create(self, serializer):
        """
        创建图片
        :param serializer: 创建图片的参数
        :return: 
        """
        return ImageService.init_save_serializer(self.request.user, serializer)


class LikeViewset(CreateDestroyModelMixin):
    """
    create:
        动作: 登录用户点赞某活动
    destroy:
        动作: 登录用户取消已点赞活动
        id: 点赞id(非活动id)
    """
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_adapter = {'all': LikeSerializer}
    no_login_methods = ()

    def make_queryset(self):
        user = self.request.user
        self.update_queryset('destroy', LikeDAL.get_like_by_user, user_id=user.id)

    def perform_create(self, serializer):
        """
        点赞
        :param serializer: 
        :return: 
        """
        serializer.validated_data['user'] = self.request.user
        return serializer.save()


class CollectViewset(CreateDestroyModelMixin):
    """
    create:
        动作: 登录用户收藏活动
    destroy:
        动作: 登录用户取消已收藏的活动
        id: 收藏id(不是活动id)
    """
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_adapter = {'all': CollectSerializer}
    no_login_methods = ()

    def make_queryset(self):
        user = self.request.user
        self.update_queryset('destroy', CollectDAL.get_collect_by_user, user_id=user.id)

    def perform_create(self, serializer):
        """
        收藏
        :param serializer: 
        :return: 
        """
        serializer.validated_data['user'] = self.request.user
        return serializer.save()


class UserGroupRefViewset(CreateListDestroyModelMixin):
    """
    list:
        获取登录用户关注的全部职业圈
    create:
        动作: 登录用户关注职业圈
    destroy:
        动作: 登录用户取消已关注的职业圈
        id: 关系id(不是职业圈id)
    """
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    no_login_methods = ()
    serializer_adapter = {
        'list': GroupSerializer,
        'other': UserGroupRefSerializer,
    }

    def make_queryset(self):
        user = self.request.user
        self.update_queryset('destroy', UserGroupRefDAL.get_ref_by_user, user_id=user.id)
        self.update_queryset('list', GroupDAL.get_group_by_user, user_id=user.id)

    def perform_create(self, serializer):
        """
        关注职业圈
        :param serializer: 
        :return: 
        """
        serializer.validated_data['user'] = self.request.user
        return serializer.save()
