from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *


app_name = 'users'

urlpatterns = [
    path("accounts/register/", UserCreateView.as_view(), name="register_user"),
    path("accounts/register-mod/", ModeratorCreateView.as_view(), name="register_moderator"),
    path("login/", MessageLoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("profile/edit/", UserProfileUpdateView.as_view(), name="profile_edit"),
]