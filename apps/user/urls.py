from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenBlacklistView, TokenRefreshView

from . import views

urlpatterns = [
    path('user/register/', views.Register.as_view(), name='user-register'),
    path('user/login/', TokenObtainPairView.as_view(), name='user-login'),
    path('user/logout/', TokenBlacklistView.as_view(), name='user-logout'),
    path('user/', views.CurrentUser.as_view(), name='current-user-detail'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]
