from .models import User


class UserDAL:
    @staticmethod
    def has_user_by_email(email):
        return User.objects.filter(email=email).count() > 0

    @staticmethod
    def has_user_by_username(username):
        return User.objects.filter(username=username).count() > 0

    @staticmethod
    def get_users_by_field(**kwargs):
        return User.objects.filter(**kwargs) if kwargs else User.objects.all()

    @staticmethod
    def create_user(**kwargs):
        User.objects.create_user(**kwargs)
