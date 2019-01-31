import functools
from rest_framework import serializers

from .exceptions import NotPermissionError


class Validation:
    @staticmethod
    def need_permission(error_msg="无权限操作！"):
        """
        抛出权限错误的函数就返回错误 json
        :param error_msg: 
        :return: 
        """
        def _func(func):
            @functools.wraps(func)
            def __func(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except NotPermissionError:
                    raise serializers.ValidationError(error_msg)
            return __func
        return _func

    @staticmethod
    def not_return_false(error_msg="操作错误！"):
        """
        返回 False 的函数就返回错误 json
        :param error_msg: 
        :return: 
        """
        def _func(func):
            @functools.wraps(func)
            def __func(*args, **kwargs):
                obj = func(*args, **kwargs)
                if obj is False:
                    raise serializers.ValidationError(error_msg)
                return obj
            return __func
        return _func
