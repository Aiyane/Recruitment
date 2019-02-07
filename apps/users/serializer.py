from rest_framework import serializers

from .models import User, Message
from .service import UserService
from utils.decorator import Validation


class MessageSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(label="用户", help_text="用户")
    sender = serializers.IntegerField(label="发送者", help_text="发送者", allow_null=True)
    text = serializers.CharField(label="内容", help_text="内容")
    data_joined = serializers.DateTimeField(label="时间", help_text="时间", read_only=True)
    had_read = serializers.BooleanField(label="已读", help_text="已读", read_only=True)

    class Meta:
        model = Message
        fields = ('user', 'sender', 'text', 'data_joined', 'had_read')


class UserPutSerializer(serializers.ModelSerializer):
    password = serializers.CharField(label="密码", help_text="密码", style={'input_type': 'password'},
                                     write_only=True, required=False)
    name = serializers.CharField(label="姓名", help_text="姓名", required=False)
    desc = serializers.CharField(label="简介", help_text="简介", required=False)
    head = serializers.ImageField(label="头像", help_text="头像", required=False)

    class Meta:
        model = User
        fields = ('password', 'name', 'desc', 'head')


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(label="用户名", help_text="用户名", required=True)
    email = serializers.EmailField(label="邮箱", help_text="邮箱", required=True)
    password = serializers.CharField(label="密码", help_text="密码", style={'input_type': 'password'}, write_only=True)
    name = serializers.CharField(label="姓名", help_text="姓名", required=False)
    fans = serializers.IntegerField(label="粉丝数", help_text="粉丝数", read_only=True)
    follows = serializers.IntegerField(label="关注者数", help_text="关注者数", read_only=True)
    desc = serializers.CharField(label="简介", help_text="简介", required=False)
    identity = serializers.IntegerField(label="身份", help_text="身份", read_only=True)
    head = serializers.ImageField(label="头像", help_text="头像", required=False)

    @Validation.not_return_false(error_msg="用户已存在！")
    def validate(self, attrs):
        """
        验证用户名与邮箱
        :param attrs: 
        :return: 
        """
        if UserService.can_create_user(attrs['username'], attrs['email']):
            return attrs
        return False

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'username', 'name', 'fans', 'follows', 'desc', 'identity', 'head')
