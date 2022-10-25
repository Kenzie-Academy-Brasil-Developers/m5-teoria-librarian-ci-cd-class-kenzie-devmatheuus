from django.urls import path
from rest_framework.authtoken.views import ObtainAuthToken, obtain_auth_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    token_obtain_pair,
    token_refresh,
)

from . import views

urlpatterns = [
    # path("librarians/login/auth_token/", views.LoginView.as_view()),
    # path("librarians/login/auth_token/", ObtainAuthToken.as_view()),
    path("librarians/login/auth_token/", obtain_auth_token, name="login-auth-token"),
    # path("librarians/login/jwt_token/", TokenObtainPairView.as_view()),
    # path("librarians/login/jwt_token/", token_obtain_pair),
    path("librarians/login/jwt_token/refresh/", TokenRefreshView.as_view()),
    path("librarians/login/jwt_token/", views.LoginJWTView.as_view()),
    path("librarians/register/", views.RegisterView.as_view()),
    # path("librarians/login/jwt_token/refresh/", token_refresh),
]
