from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group



User = get_user_model()



class RegisterUserForm(UserCreationForm):

    email = forms.EmailField(required=True, help_text="Inserisci un indirizzo email valido.")
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")



class RegisterModeratorForm(RegisterUserForm):

    def save(self, commit=True):
        user = super().save(commit=commit)
        # get_or_create restituisce una tupla (oggetto, creato_ora)
        group, created = Group.objects.get_or_create(name="Moderators")
        
        if commit:
            user.groups.add(group)
        else:
            # Django salva i gruppi dopo il save_m2m()
            old_save_m2m = self.save_m2m
            def save_m2m():
                old_save_m2m()
                user.groups.add(group)
            self.save_m2m = save_m2m
            
        return user