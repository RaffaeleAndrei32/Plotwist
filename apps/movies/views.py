from django.views.generic import CreateView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy

from .models import Movie
from .forms import MovieForm

class MovieCreateView(UserPassesTestMixin, CreateView):
    model = Movie
    form_class = MovieForm
    template_name = 'movies/add_movie.html'
    success_url = reverse_lazy('home')

    # Controllo permessi: solo Staff o Moderatori
    def test_func(self):
        return self.request.user.is_staff or self.request.user.groups.filter(name='Moderators').exists()

    # Salvataggio automatico dell'utente loggato
    def form_valid(self, form):
        form.instance.logged_by = self.request.user
        return super().form_valid(form)