from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import LoginSerializer, GroupSerializer, UserSerializer, CreateGroupSerializer, PermissionSerializer

User = get_user_model()


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


class UserViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    """
    Manage users
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(
        detail=False,
        methods=['get', 'post'],
    )
    def groups(self, request):
        if request.method == 'POST':
            # TODO: set user groups
            return Response({})
        return Response(GroupSerializer(Group.objects.filter(user=request.user), many=True).data)

    @action(
        detail=False,
        methods=['get', 'post'],
    )
    def permissions(self, request):
        if request.method == 'POST':
            # TODO: set user permissions
            return Response({})

        user = request.user
        if user.is_superuser:
            permissions = Permission.objects.all()
        else:
            permissions = list(user.user_permissions.all() | Permission.objects.filter(group__user=user))
        return Response(PermissionSerializer(permissions, many=True).data)


class GroupViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    """
    Manage user groups
    """
    queryset = Group.objects.all()
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateGroupSerializer
        return GroupSerializer
