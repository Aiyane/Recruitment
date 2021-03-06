from rest_framework import serializers

from .models import Activity, Image, Like, Collect, Group, UserGroupRef
from .service import ActivityService
from users.serializer import UserSerializer
from utils.decorator import Validation


class UserGroupRefSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(label="用户", help_text="用户", required=True)
    group = serializers.IntegerField(label="职业圈", help_text="职业圈", required=True)
    date_joined = serializers.DateTimeField(label="时间", help_text="时间", read_only=True)

    class Meta:
        model = UserGroupRef
        fields = ('user', 'group', 'date_joined')


class GroupSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(label="图片", help_text="图片", read_only=True)
    name = serializers.CharField(label="名字", help_text="名字", read_only=True)

    class Meta:
        model = Group
        fields = ('image', 'name', 'id')


class CollectSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(label="用户", help_text="用户", required=True)
    activity = serializers.IntegerField(label="活动", help_text="活动", required=True)
    date_joined = serializers.DateTimeField(label="时间", help_text="时间", read_only=True)

    class Meta:
        model = Collect
        fields = ('user', 'activity', 'date_joined', 'id')


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(label="用户", help_text="用户", required=True)
    activity = serializers.IntegerField(label="活动", help_text="活动", required=True)
    date_joined = serializers.DateTimeField(label="时间", help_text="时间", read_only=True)

    class Meta:
        model = Like
        fields = ('user', 'activity', 'date_joined', 'id')


class ImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(label="图片", help_text="图片", required=True)
    date_joined = serializers.DateTimeField(label="添加时间", help_text="添加时间", read_only=True)
    activity = serializers.IntegerField(label="活动", help_text="活动", write_only=True)

    @Validation.not_return_false("没有创建权限！")
    def validate(self, attrs):
        if ActivityService.is_user_activity(self.context['request'].user, int(attrs['activity'])):
            return attrs
        return False

    class Meta:
        model = Image
        fields = ('image', 'date_joined', 'activity')


class ActivitySerializer(serializers.ModelSerializer):
    status = serializers.IntegerField(label="状态", help_text="状态", read_only=True)
    text = serializers.CharField(label="文本", help_text="文本", required=False)
    date_joined = serializers.DateTimeField(label="添加时间", help_text="添加时间", read_only=True)
    start_time = serializers.DateTimeField(label="开始时间", help_text="开始时间", read_only=True)
    end_time = serializers.DateTimeField(label="结束时间", help_text="结束时间", read_only=True)
    likes = serializers.IntegerField(label="点赞数", help_text="点赞数", read_only=True)
    comments = serializers.IntegerField(label="评论数", help_text="评论数", read_only=True)
    collects = serializers.IntegerField(label="收藏数", help_text="收藏数", read_only=True)
    user = UserSerializer(required=False)
    classification = serializers.IntegerField(label="类型", help_text="类型", required=True)
    images = ImageSerializer(many=True)

    class Meta:
        model = Activity
        fields = ('id', 'status', 'text', 'date_joined', 'start_time', 'images',
                  'end_time', 'likes', 'comments', 'collects', 'user', 'classification')
