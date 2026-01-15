from django.shortcuts import render
from apps.movies.models import Movie
from django.db.models import Avg




def home(request):
    # 1. Prendi tutti i film
    # 2. Crea un campo temporaneo 'avg_rating' calcolando la media delle recensioni
    # 3. Ordina per quel campo (il '-' indica ordine decrescente)
    # 4. Prendi i primi 6
    top_movies = Movie.objects.annotate(
        avg_rating=Avg('reviews__rating')
    ).order_by('-avg_rating')[:50]
    context = {'top_movies': top_movies}
    return render(request, template_name="home.html", context=context)