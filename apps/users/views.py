from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication

from .serializer import UserSerializer, UserPutSerializer, MessageSerializer, FollowSerializer
from .dal import UserDAL, MessageDAL, FollowDAL
from .service import UserService
from utils import viewsets


class UserViewset(viewsets.NoDestroyModelMixin):
    """
    list:
        不需要登录，获取全部用户信息
    retrieve:
        不需要登录，获取某个用户信息
    update:
        登录用户修改个人信息
    partial_update:
        登录用户修改个人信息
    create:
        注册用户
    """
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    no_login_methods = ('create', 'retrieve', 'list')
    service_class = UserService
    serializer_adapter = {
        'update': UserPutSerializer,
        'partial_update': UserPutSerializer,
        'other': UserSerializer
    }

    def make_queryset(self):
        user = self.request.user
        self.update_queryset('list', UserDAL.get_users_by_field, is_active=True)
        self.update_queryset('retrieve', UserDAL.get_users_by_field, is_active=True)
        self.update_queryset('update', UserDAL.get_users_by_field, id=user.id)
        self.update_queryset('partial_update', UserDAL.get_users_by_field, id=user.id)

    def perform_create(self, serializer):
        """
        创建用户，使用自定义的，可以对密码加密
        :param serializer: 用户参数
        :return: 
        """
        return UserDAL.create_user(**serializer.validated_data)


class MessageViewset(viewsets.ReadOnlyModelViewSet):
    """
    list:
        登录用户获取个人信息
    retrieve:
        登录用户获取某个信息的详情
    """
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    no_login_methods = []
    serializer_adapter = {'all': MessageSerializer}

    def make_queryset(self):
        user = self.request.user
        self.update_queryset('list', MessageDAL.get_messages_by_user, user_id=user.id)
        self.update_queryset('retrieve', MessageDAL.get_messages_by_user, user_id=user.id)


class FollowViewset(viewsets.CreateDestroyModelMixin):
    """
    create:
        动作: 登录用户关注某用户
    destroy:
        动作: 登录用户取消关注已关注用户
        id: 关注id(不是用户id)
    """
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    no_login_method = ()
    serializer_adapter = {'all': FollowSerializer}

    def make_queryset(self):
        user = self.request.user
        self.update_queryset('destroy', FollowDAL.get_follow_by_user, user_id=user.id)
