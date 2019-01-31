from .models import Activity


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
