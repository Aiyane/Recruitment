from rest_framework import serializers

from .models import User
from .service import UserService


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

    def validate(self, attrs):
        email = attrs['email']
        username = attrs['username']
        can, msg = UserService.can_create_user(username, email)
        if not can:
            raise serializers.ValidationError(msg)
        return attrs

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'username', 'name', 'fans', 'follows', 'desc', 'identity', 'head')
