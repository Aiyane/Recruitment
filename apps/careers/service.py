from utils.const import CreateDynamicPermission, ActivityType
from utils.service import BaseService
from utils.exceptions import NotPermissionError
from .dal import ActivityDAL


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
    def is_user_activity(user, activity):
        """
        判断是否是该用户创建的活动
        :param user: 用户
        :param activity: 相关活动
        :return: 
        """
        if user.id == activity.user_id:
            return True
        raise False
