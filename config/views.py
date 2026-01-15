from django.shortcuts import render
from apps.movies.models import Movie
from django.db.models import Avg



def home(request):
    top_movies = Movie.objects.annotate(
        avg_rating=Avg('reviews__rating')
    ).order_by('-avg_rating')[:50]
    context = {'top_movies': top_movies}

    return render(request, template_name="home.html", context=context)