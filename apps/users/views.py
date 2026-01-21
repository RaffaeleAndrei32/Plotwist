from django.views.generic.edit import CreateView, UpdateView
from .forms import ExtendedUserCreationForm, ModeratorCreationForm, UserProfileForm
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin



class MessageLoginView(LoginView):
    template_name = 'registration/login.html'
    
    # Override form_valid to add a success message upon login
    def form_valid(self, form):
        messages.success(self.request, "Congratulations! You have successfully logged in.")
        response = super().form_valid(form)
        return response



class UserCreateView(CreateView):       
    form_class = ExtendedUserCreationForm
    template_name = "registration/register_user.html"
    success_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_type'] = "user"
        return context



class ModeratorCreateView(CreateView):       
    form_class = ModeratorCreationForm
    template_name = "registration/register_user.html"
    success_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_type'] = "moderator"
        return context


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    """View for users to update their profile."""
    form_class = UserProfileForm
    template_name = 'users/profile_edit.html'
    success_url = reverse_lazy('users:profile_edit')
    login_url = 'login'
    
    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, "Profile updated successfully!")
        return super().form_valid(form)