from utils.const import CreateDynamicPermission, ActivityType
from utils.service import BaseService
from utils.exceptions import NotPermissionError
from .dal import ActivityDAL, GroupDAL, UserGroupRefDAL
from .models import ActivityGroupRef


class ActivityService(BaseService):
    """
    创建活动对应的方法
    """
    create_activity_dals = {
        ActivityType.RECRUITMENT: ActivityDAL.create_recruitment,
        ActivityType.MATCH: ActivityDAL.create_match,
        ActivityType.DYNAMIC: ActivityDAL.create_dynamic,
        ActivityType.INTRODUCTION: ActivityDAL.create_introduction,
    }

    @staticmethod
    def create(request, instance):
        """
        创建活动之后的操作，如果带有职业圈，添加活动与职业圈之间的关联
        :param request: 
        :param instance: 
        :return: 
        """
        if 'group' in request.POST:
            group_id = int(request.POST['group'])
            if GroupDAL.has_group_by_id(group_id):
                user_id = request.user
                if UserGroupRefDAL.has_ref_by_user_group(user_id, group_id):
                    ActivityGroupRef(activity_id=instance.id, group_id=group_id).save()
                    return instance
        return instance

    @staticmethod
    def create_activity(identity, activity, **fields):
        """
        创建活动，没有权限抛出错误
        :param identity: 用户身份
        :param activity: 需要创建的活动
        :param fields: 创建活动需要的条件
        :return: 
        """
        if activity not in CreateDynamicPermission[identity]:
            raise NotPermissionError("你没有创建%s的权限！" % dict(ActivityType.TYPE)[activity])
        return ActivityService.create_activity_dals[activity](**fields)

    @staticmethod
    def is_user_activity(user, activity_id):
        """
        判断是否是该用户创建的活动
        :param user: 用户
        :param activity: 相关活动
        :return: 
        """
        activity = ActivityDAL.get_activity_by_id(activity_id)
        if user.id == activity.user_id:
            return True
        raise False


class ImageService(BaseService):
    @staticmethod
    def init_save_serializer(user, serializer):
        """
        新建图片
        :param user: 
        :param serializer: 
        :return: 
        """
        serializer.validated_data['user'] = user
        activity_id = serializer.validated_data['activity']
        serializer.validated_data['activity'] = ActivityDAL.get_activity_by_id(activity_id)
        return serializer.save()
