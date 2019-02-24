from .models import Activity, Group, UserGroupRef, Like, Collect


class UserGroupRefDAL:
    @staticmethod
    def has_ref_by_user_group(user_id, group_id):
        return UserGroupRef.objects.filter(user_id=user_id, group_id=group_id).count() > 0

    @staticmethod
    def get_ref_by_user(user_id):
        return UserGroupRef.objects.filter(user_id=user_id)


class GroupDAL:
    @staticmethod
    def has_group_by_id(group_id):
        return Group.objects.filter(id=group_id).count() > 0

    @staticmethod
    def get_group_by_id(group_id):
        return Group.objects.filter(id=group_id).first()

    @staticmethod
    def get_group_by_user(user_id):
        return Group.objects.filter(id__in=UserGroupRef.objects.filter(user_id=user_id).values_list(id, flat=True))


class CollectDAL:
    @staticmethod
    def get_collect_by_user(user_id):
        return Collect.objects.filter(user_id=user_id)


class LikeDAL:
    @staticmethod
    def get_like_by_user(user_id):
        return Like.objects.filter(user_id=user_id)


class ActivityDAL:
    @staticmethod
    def get_activity_by_field(**kwargs):
        return Activity.objects.filter(**kwargs) if kwargs else Activity.objects.all()

    @staticmethod
    def get_activity_by_id(activity_id):
        return Activity.objects.get(id=activity_id)

    @staticmethod
    def create_match(start_time_str, end_time_str, **extra_fields):
        return Activity.objects.create_match(start_time_str, end_time_str, **extra_fields)

    @staticmethod
    def create_dynamic(**fields):
        return Activity.objects.create_dynamic(**fields)

    @staticmethod
    def create_introduction(**fields):
        return Activity.objects.create_dynamic(**fields)

    @staticmethod
    def create_recruitment(**fields):
        return Activity.objects.create_recruitment(**fields)
