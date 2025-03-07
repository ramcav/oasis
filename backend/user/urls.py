from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib import admin
from django.urls import path, include

from .views import register, CustomTokenObtainPairView, CustomTokenRefreshView, UserListView, UserDeleteView


urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path("register/", register, name="register_user"),
    path("users/", UserListView.as_view(), name="user_list"),
    path("users/<int:pk>/", UserDeleteView.as_view(), name="user_delete"),
]