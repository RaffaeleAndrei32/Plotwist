from django.contrib import admin
from .models import Movie, Genre, Director, Actor
from .forms import MovieForm



class MovieAdmin(admin.ModelAdmin):
    form = MovieForm

    filter_horizontal = ('actors', 'genres')
    list_display = ('title', 'release_date', 'director')
    list_filter = ('genres', 'release_date')
    search_fields = ('title',)




admin.site.register(Movie, MovieAdmin)

admin.site.register([Genre, Director, Actor])