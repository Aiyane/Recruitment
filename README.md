## Django REST framework 项目示例

本项目在 `apps/utils/mixins.py`、`apps/utils/service.py`、`apps/utils/viewsets.py` 三个文件中对 `Django REST framework` 进行了部分封装。使得可以在 `viewset` 中使用特殊的语法。

例如在 `apps/users/views.py` 的 `UserViewset` 类中

```py
class UserViewset(NoDestroyModelMixin):
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    no_login_methods = ('create', 'retrieve', 'list')
    serializer_adapter = {'all': UserSerializer}
    service_class = UserService

    def make_queryset(self):
        user = self.request.user
        self.update_queryset('list', UserDAL.get_users_by_field, is_active=True)
        self.update_queryset('retrieve', UserDAL.get_users_by_field, is_active=True)
        self.update_queryset('update', UserDAL.get_users_by_field, id=user.id)
        self.update_queryset('partial_update', UserDAL.get_users_by_field, id=user.id)

    def perform_create(self, serializer):
        return UserDAL.create_user(**serializer.validated_data)
```

`no_login_methods` 存放不需要登录的方法，`serializer_adapter` 是一个 **方法-序列化类** 字典，可以使用 `all` 或者 `other` 这样的 key 来避免重复写。当然最一般的就是
```py
serializer_adapter = {'create': UserSerializer,
                      'list': UserListSerializer,
                      'other': UserOtherSerializer}
```
这种写法。

`make_queryset` 方法替代了以前的 `get_queryset_class` 但是用法完全变了。使用 `self.update_queryset` 函数传递方法对应的查询函数，第三个及之后的参数是查询函数需要的参数，当然也可以不填。

然后是 `service_class` 属性，该属性对应一个 `BaseService` 的子类，可以查看 `apps/utils/service.py` 中的源代码。
```py
class BaseService:
    @staticmethod
    def list(request, queryset):
        """过滤后,还需要过滤"""
        return queryset

    @staticmethod
    def create(request, instance):
        """新建对象后,还需要处理"""
        return instance

    @staticmethod
    def update(request, instance):
        """更新后,需要做些处理"""
        return instance

    @staticmethod
    def partial_update(request, instance):
        """更新后,需要做些处理"""
        return instance

    @staticmethod
    def destroy(request, instance):
        """删除前,需要做些处理"""
        return instance
```
如上所示，继承 `BaseService` 类，覆盖上述五个方法中的任意方法，在函数内部就可以做一些相应的处理。就如 `apps/users/service.py` 中的 `UserService` 类一样。

这样处理的结果使得数据与逻辑分离，代码也更加简洁易懂。