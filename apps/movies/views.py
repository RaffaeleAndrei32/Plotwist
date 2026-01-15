from multiprocessing import context
from django.views.generic import CreateView, ListView, DetailView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.views import View

from .models import Movie
from .forms import MovieForm, DATE_MIN
from django_filters.views import FilterView
from .filters import MovieFilter



class MovieListView(FilterView):
    model = Movie
    template_name = 'movies/movies_list.html'
    filterset_class = MovieFilter
    context_object_name = 'movies'
    paginate_by = 9



class MovieDetailView(DetailView):
    model = Movie
    template_name = 'movies/movie_info.html'
    context_object_name = 'movie'
    pk_url_kwarg = 'pk'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            context['in_watchlist'] = self.object.watched_by.filter(id=self.request.user.id).exists()
            
            context['user_review'] = self.object.reviews.filter(user=self.request.user).first()
        
        context['reviews'] = self.object.reviews.all()
        
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


class UserMoviesListView(LoginRequiredMixin, ListView):
    model = Movie
    template_name = 'movies/user_movies_list.html'
    context_object_name = 'movies'
    paginate_by = 9
    login_url = 'accounts:login'
    
    def get_queryset(self):
        return Movie.objects.filter(logged_by=self.request.user).select_related('director', 'logged_by')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'My Movies'
        return context