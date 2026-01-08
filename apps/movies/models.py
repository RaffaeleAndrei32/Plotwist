from django.db import models
from django.core.validators import MinValueValidator
from django.conf import settings



class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name



class Actor(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)

    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} {self.surname}"



class Director(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} {self.surname}"



class Movie(models.Model):
    title = models.CharField(max_length=200)
    release_date = models.DateField()
 
    length = models.IntegerField(
        help_text="Length in minutes",
        validators=[MinValueValidator(1)]
    )

    director = models.ForeignKey(
        Director, 
        on_delete=models.CASCADE, 
        related_name='movies'
    )
    
    logged_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='movies_added'
    )
    
    actors = models.ManyToManyField(Actor, related_name='movies')
    genres = models.ManyToManyField(Genre, related_name='movies')
    
    watched_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        related_name='watched_movies', 
        blank=True
    )
    
    def __str__(self):
        return self.title

    def clean(self):
        super().clean()
        # Qui potrai aggiungere i tuoi controlli personalizzati 
        # (es. il limite dei 3 generi che abbiamo discusso)