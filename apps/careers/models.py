from django.db import models
from django.utils import timezone
from datetime import datetime

from users.models import User
from utils.storage import ImageStorage
from utils.const import ActivityStatus, ActivityType, Action


class Group(models.Model):
    superior = models.IntegerField(verbose_name="上级id", default=0)
    image = models.ImageField(upload_to="group/%Y/%m", storage=ImageStorage(), verbose_name="图片")
    name = models.CharField(verbose_name="名字", max_length=20, unique=True)
    date_joined = models.DateTimeField(verbose_name="添加时间", default=timezone.now)

    class Meta:
        db_table = 'group'
        verbose_name = "职业圈"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class ActivityManager(models.Manager):
    def _create_object(self, **fields):
        obj = self.model(**fields)
        obj.save(using=self._db)
        return obj

    def create_match(self, start_time_str, end_time_str, **extra_fields):
        extra_fields['classification'] = ActivityType.MATCH
        now = datetime.now()
        start_time = datetime.strptime(start_time_str, '%Y-%m-%d %H:%M')
        end_time = datetime.strptime(end_time_str, '%Y-%m-%d %H:%M')

        if end_time < now:
            extra_fields['status'] = ActivityStatus.END
        else:
            if start_time < now:
                extra_fields['status'] = ActivityStatus.PROCESSING
            else:
                extra_fields['status'] = ActivityStatus.PREPARING
                # TODO: 添加两个定时任务，在开始时间将状态变成“PROCESSING”
            # TODO: 添加定时任务，在结束时间时将状态改变成“END”
        return self._create_object(start_time=start_time, end_time=end_time, **extra_fields)

    def create_dynamic(self, **fields):
        fields['classification'] = ActivityType.DYNAMIC
        return self._create_object(**fields)

    def create_introduction(self, **fields):
        fields['classification'] = ActivityType.INTRODUCTION
        return self._create_object(**fields)

    def create_recruitment(self, **fields):
        fields['classification'] = ActivityType.RECRUITMENT
        return self._create_object(**fields)


class Activity(models.Model):
    classification = models.IntegerField(verbose_name="类型", choices=ActivityType.TYPE)
    status = models.IntegerField(verbose_name="状态", default=ActivityStatus.NO, choices=ActivityStatus.TYPE)
    text = models.TextField(verbose_name="文本")
    date_joined = models.DateTimeField(verbose_name="添加时间", default=timezone.now)
    start_time = models.DateTimeField(verbose_name="开始时间", null=True, blank=True)
    end_time = models.DateTimeField(verbose_name="结束时间", null=True, blank=True)
    likes = models.IntegerField(verbose_name="点赞数", default=0)
    comments = models.IntegerField(verbose_name="评论数", default=0)
    collects = models.IntegerField(verbose_name="收藏数", default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="创建者")

    objects = ActivityManager()

    class Meta:
        db_table = "activity"
        verbose_name = "活动"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.id


class Image(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, verbose_name="动态", related_name="images")
    image = models.ImageField(verbose_name="图片", upload_to="activity/%Y/%m", storage=ImageStorage())
    user = models.ForeignKey(User, verbose_name="用户", on_delete=models.SET_NULL, null=True, blank=True)
    date_joined = models.DateTimeField(verbose_name="添加时间", default=timezone.now)

    class Meta:
        db_table = "image"
        verbose_name = "图片"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.id


class DynamicGroupRef(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, verbose_name="活动")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name="职业圈")
    date_joined = models.DateTimeField(verbose_name="添加时间", default=timezone.now)

    class Meta:
        db_table = "activity_group_ref"

    def __str__(self):
        return self.id


class UserActivityRef(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, verbose_name="活动")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="用户")
    action = models.IntegerField(verbose_name="操作类型", choices=Action.TYPE)
    data_joined = models.DateTimeField(verbose_name="添加时间", default=timezone.now)

    class Meta:
        db_table = "user_activity_ref"

    def __str__(self):
        return self.id


class Comment(models.Model):
    text = models.CharField(verbose_name="内容", max_length=100)
    superior = models.IntegerField(verbose_name="上级id", default=0)
    data_joined = models.DateTimeField(verbose_name="添加时间", default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="用户")
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, verbose_name="活动")

    class Meta:
        db_table = "comment"

    def __str__(self):
        return self.id
