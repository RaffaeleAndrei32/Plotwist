from django.views.generic import CreateView, ListView, DetailView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404
from django.views import View
import datetime

from .models import Movie, Director, Genre
from .forms import MovieForm



class MovieListView(ListView):
    model = Movie
    template_name = 'movies/movies_list.html'
    context_object_name = 'movies'
    paginate_by = 9
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['directors'] = Director.objects.all()
        context['genres'] = Genre.objects.all()
        
        current_year = datetime.date.today().year
        context['years'] = range(1870, current_year + 10, 10)
        
        return context
    
    def get_queryset(self):
        queryset = Movie.objects.all()
        
        # Filtro per ricerca titolo
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(title__icontains=search)
        
        genre_id = self.request.GET.get('genre')
        if genre_id:
            queryset = queryset.filter(genres__id=genre_id)
        
        director_id = self.request.GET.get('director')
        if director_id:
            queryset = queryset.filter(director__id=director_id)
        
        year = self.request.GET.get('year')
        if year:
            year_int = int(year)
            decade_end = year_int + 9
            queryset = queryset.filter(release_date__year__gte=year_int, release_date__year__lte=decade_end)
        
        return queryset.distinct()



class MovieDetailView(DetailView):
    model = Movie
    template_name = 'movies/movie_info.html'
    context_object_name = 'movie'
    pk_url_kwarg = 'pk'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Controlla se l'utente ha aggiunto questo film alla watchlist
        if self.request.user.is_authenticated:
            context['in_watchlist'] = self.object.watched_by.filter(id=self.request.user.id).exists()
        return context



class MovieCreateView(UserPassesTestMixin, CreateView):
    model = Movie
    form_class = MovieForm
    template_name = 'movies/add_movie.html'
    success_url = reverse_lazy('movies:list_movies')

    def test_func(self):
        return self.request.user.is_staff or self.request.user.groups.filter(name='Moderators').exists()

    def form_valid(self, form):
        form.instance.logged_by = self.request.user
        return super().form_valid(form)



class WatchlistView(LoginRequiredMixin, ListView):
    model = Movie
    template_name = 'movies/watchlist.html'
    context_object_name = 'movies'
    paginate_by = 9
    login_url = 'login'
    
    def get_queryset(self):
        return self.request.user.watched_movies.all()



class AddToWatchlistView(LoginRequiredMixin, View):
    login_url = 'login'
    
    def post(self, request, pk):
        movie = get_object_or_404(Movie, pk=pk)
        movie.watched_by.add(request.user)
        return redirect('movies:watchlist')



class RemoveFromWatchlistView(LoginRequiredMixin, View):
    login_url = 'login'
    
    def post(self, request, pk):
        movie = get_object_or_404(Movie, pk=pk)
        movie.watched_by.remove(request.user)
        return redirect('movies:watchlist')