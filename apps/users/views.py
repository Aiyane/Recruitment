from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication

from .serializer import UserSerializer
from .dal import UserDAL
from .service import UserService
from utils.viewsets import NoDestroyModelMixin


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
