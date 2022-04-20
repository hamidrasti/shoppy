from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views

from accounts.views import LoginView, AuthViewSet

app_name = 'accounts'

router = DefaultRouter()
router.register('', AuthViewSet, basename='auth')

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('refresh/', views.TokenRefreshView.as_view(), name='refresh'),
    path('', include(router.urls)),
]
