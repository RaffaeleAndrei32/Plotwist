from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy

from .models import Movie
from .forms import MovieForm



class MovieListView(ListView):
    model = Movie
    template_name = 'movies/movie_list.html'
    context_object_name = 'movies'
    paginate_by = 9



class MovieCreateView(UserPassesTestMixin, CreateView):
    model = Movie
    form_class = MovieForm
    template_name = 'movies/add_movie.html'
    success_url = reverse_lazy('movies:list_movies')

    # Controllo permessi: solo Staff o Moderatori
    def test_func(self):
        return self.request.user.is_staff or self.request.user.groups.filter(name='Moderators').exists()

    # Salvataggio automatico dell'utente loggato
    def form_valid(self, form):
        form.instance.logged_by = self.request.user
        return super().form_valid(form)