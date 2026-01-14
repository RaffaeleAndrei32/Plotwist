from django import forms
from .models import Movie
from datetime import date



DATE_MIN = date(1895, 12, 28)



class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie

        fields = ['title', 'release_date', 'length', 'director', 'actors', 'genres', 'poster', 'plot']

        widgets = {
            'release_date': forms.SelectDateWidget(
            years=list(range(DATE_MIN.year, date.today().year + 1)), 
            attrs={'class': 'form-control d-inline-block w-auto'}
    ),

            'title': forms.TextInput(),
            'length': forms.NumberInput(attrs={'min': '1'}),
            'director': forms.Select(),
            'actors': forms.SelectMultiple(),
            'genres': forms.SelectMultiple(),
            'poster': forms.FileInput(attrs={'accept': 'image/*'}),
            'plot': forms.Textarea(attrs={'rows': 4}),
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