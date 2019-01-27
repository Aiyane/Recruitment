from utils.service import BaseService
from .dal import UserDAL


class UserService(BaseService):
    @staticmethod
    def can_create_user(username, email):
        if UserDAL.has_user_by_username(username):
            return False, '用户名已经存在！'
        if UserDAL.has_user_by_email(email):
            return False, '邮箱已经存在！'
        return True, ''
