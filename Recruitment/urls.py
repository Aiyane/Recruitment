"""Recruitment URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

import xadmin
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls

from users.views import UserViewset, MessageViewset
from careers.views import ActivityViewset, ImageViewset, LikeViewset, CollectViewset, UserGroupRefViewset

router = DefaultRouter()
router.register('users', UserViewset, base_name="users")
router.register('activities', ActivityViewset, base_name="activities")
router.register('images', ImageViewset, base_name="images")
router.register('messages', MessageViewset, base_name="messages")
router.register('likes', LikeViewset, base_name="likes")
router.register('collects', CollectViewset, base_name="collects")
# 用户关注的职业圈，关注职业圈(动作)，取消关注职业圈(动作)
router.register('attentions', UserGroupRefViewset, base_name="attentions")

urlpatterns = [
    # 后台管理
    path('admin/', xadmin.site.urls),
    # 登录
    path('login/', obtain_jwt_token),
    path('', include(router.urls)),
    path('docs/', include_docs_urls(title="求职系统")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
