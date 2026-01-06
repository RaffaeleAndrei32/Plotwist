from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model



User = get_user_model()



class ExtendedUserCreationForm(UserCreationForm):

    email = forms.EmailField(
        required=True, 
        help_text="Inserisci un indirizzo email valido."
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")



class ModeratorCreationForm(ExtendedUserCreationForm):
    
    def save(self, commit=True):
        user = super().save(commit) 
        #g = Group.objects.get(name="Moderators") 
        group, created = Group.objects.get_or_create(name="Moderators")
        group.user_set.add(user) 
        return user 
   