from utils.service import BaseService
from .dal import UserDAL, MessageDAL
from utils.const import MessageContent


class UserService(BaseService):
    @staticmethod
    def can_create_user(username, email):
        if UserDAL.has_user_by_username(username):
            return False, '用户名已经存在！'
        if UserDAL.has_user_by_email(email):
            return False, '邮箱已经存在！'
        return True, ''

    @staticmethod
    def create(request, instance):
        # 新建用户后，新增用户注册消息
        MessageService.add_user_register_msg(instance)


class MessageService(BaseService):
    @staticmethod
    def add_user_register_msg(user):
        # 新增用户注册消息
        return MessageDAL.add_no_sender_message(user.id, MessageContent.REGISTER)
