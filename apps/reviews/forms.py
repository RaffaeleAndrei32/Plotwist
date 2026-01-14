from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review

        fields = ['title', 'text', 'rating']

        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Review title', 'maxlength': '200'}),
            'text': forms.Textarea(attrs={'placeholder': 'Write your review...', 'rows': 5}),
            'rating': forms.Select(choices=[(i, i) for i in range(1, 11)]),
        }
