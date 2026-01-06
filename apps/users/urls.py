from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *



urlpatterns = [
    path("register-u/", UserCreateView.as_view(), name="register_user"),
    path("register-m/", ModeratorCreateView.as_view(), name="register_moderator"),

    path("login/", auth_views.LoginView.as_view(template_name='users/login.html'), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]