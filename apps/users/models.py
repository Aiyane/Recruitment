from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager

from utils.const import Role
from utils.storage import ImageStorage


class ManagerUser(UserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields['is_active'] = False
        extra_fields['is_superuser'] = False
        extra_fields['is_staff'] = False
        return self._create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    name = models.CharField(verbose_name="姓名", max_length=10, null=True, blank=True)
    follows = models.IntegerField(verbose_name="关注者数", default=0)
    fans = models.IntegerField(verbose_name="粉丝数", default=0)
    desc = models.CharField(verbose_name="简介", max_length=150, blank=True)
    identity = models.IntegerField(verbose_name="身份", choices=Role.TYPE, default=Role.ORDINARY)
    head = models.ImageField(
        upload_to="heads/%Y/%m",
        default="heads/default.png", null=True, blank=True,
        storage=ImageStorage(),
        max_length=100,
        verbose_name="头像"
    )

    objects = ManagerUser()

    class Meta:
        db_table = "user"
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.id
