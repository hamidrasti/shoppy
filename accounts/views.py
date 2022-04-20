from django.contrib.auth import get_user_model
from rest_framework import viewsets, mixins
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import LoginSerializer

User = get_user_model()


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


class AuthViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    """
    Accounts ViewSet for register and manage users
    """
    queryset = User.objects.all()
