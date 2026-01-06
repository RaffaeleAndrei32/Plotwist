from django.views.generic.edit import CreateView
from .forms import ExtendedUserCreationForm, ModeratorCreationForm
from django.urls import reverse_lazy



# Create your views here.
class UserCreateView(CreateView):       
    form_class = ExtendedUserCreationForm
    template_name = "users/register_user.html"
    success_url = reverse_lazy("home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_type'] = "user"
        return context



class ModeratorCreateView(CreateView):       
    form_class = ModeratorCreationForm
    template_name = "users/register_user.html"
    success_url = reverse_lazy("home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_type'] = "moderator"
        return context