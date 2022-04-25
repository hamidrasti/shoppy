from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views

from accounts.views import LoginView, UserViewSet, GroupViewSet

app_name = 'accounts'

router = DefaultRouter()
router.register('groups', GroupViewSet, basename='groups')
router.register('', UserViewSet, basename='users')

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('refresh/', views.TokenRefreshView.as_view(), name='refresh'),
    path('', include(router.urls)),
]
