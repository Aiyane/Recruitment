from rest_framework import serializers

from .models import Activity, Image
from users.serializer import UserSerializer


class ImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(label="图片", help_text="图片", required=True)
    date_joined = serializers.DateTimeField(label="添加时间", help_text="添加时间", read_only=True)
    activity = serializers.IntegerField(label="活动", help_text="活动", write_only=True)

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
