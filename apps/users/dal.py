from .models import User, Message, Follow


class FollowDAL:
    @staticmethod
    def get_follow_by_user(user_id):
        return Follow.objects.filter(user_id=user_id)


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
        return User.objects.create_user(**kwargs)


class MessageDAL:
    @staticmethod
    def add_message(user_id, sender_id, text):
        message = Message(user_id=user_id, sender_id=sender_id, text=text)
        message.save()
        return message

    @staticmethod
    def add_no_sender_message(user_id, text):
        message = Message(user_id=user_id, text=text)
        message.save()
        return message

    @staticmethod
    def get_messages_by_user(user_id):
        return MessageDAL.get_messages_by_field(user_id=user_id)

    @staticmethod
    def get_messages_by_field(**kwargs):
        return Message.objects.filter(**kwargs) if kwargs else Message.objects.all()
