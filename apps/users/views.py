from django.shortcuts import render
from django.views.generic.edit import CreateView
from .forms import RegisterUserForm
from django.urls import reverse_lazy



# Create your views here.
class UserCreateView(CreateView):       
    form_class = RegisterUserForm
    template_name = "users/register_user.html"
    success_url = reverse_lazy("home")



class ModeratorCreateView(CreateView):       
    form_class = RegisterUserForm
    template_name = "users/register_moderator.html"
    success_url = reverse_lazy("home")