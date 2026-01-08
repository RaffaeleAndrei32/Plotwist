from django import forms
from .models import Movie
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div, Submit


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie

        fields = ['title', 'release_date', 'length', 'director', 'actors', 'genres']
        widgets = {
            'release_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'length': forms.NumberInput(attrs={'class': 'form-control'}),
            'director': forms.Select(attrs={'class': 'form-select'}),
            'actors': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'genres': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }

    def clean_genres(self):
        genres = self.cleaned_data.get('genres')

        if genres and genres.count() > 3:
            raise forms.ValidationError("You can select max 3 genres.")
        
        return genres

    def clean_length(self):
        length = self.cleaned_data.get('length')

        if length is not None and length < 0:
            raise forms.ValidationError("Movie length cannot be negative.")
        
        return length