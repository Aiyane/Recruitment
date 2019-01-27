from utils.const import CreateDynamicPermission, ActivityType
from utils.service import BaseService
from .dal import ActivityDAL


class DynamicService(BaseService):
    create_activity_dals = {
        ActivityType.RECRUITMENT: ActivityDAL.create_recruitment,
        ActivityType.MATCH: ActivityDAL.create_match,
        ActivityType.DYNAMIC: ActivityDAL.create_dynamic,
        ActivityType.INTRODUCTION: ActivityDAL.create_introduction,
    }

    @staticmethod
    def create_dynamic(identity, activity, **fields):
        if activity not in CreateDynamicPermission[identity]:
            return None, '你没有创建%s的权限！' % dict(ActivityType.TYPE)[activity]
        return DynamicService.create_activity_dals[activity](**fields), ''
