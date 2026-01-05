from django.urls import path
from .views import *



urlpatterns = [
    path("register-u/", UserCreateView.as_view(), name="register_user"),
    path("register-m/", ModeratorCreateView.as_view(), name="register_moderator"),
]