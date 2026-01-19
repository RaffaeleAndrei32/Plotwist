from datetime import date

from django.db.models import Avg
from django.views.generic import TemplateView

from apps.movies.models import Movie


class HomeView(TemplateView):
    template_name = "home.html"
    number_of_top_movies = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        period = self.request.GET.get('period', 'all')
        today = date.today()

        movies = Movie.objects.annotate(avg_rating=Avg('reviews__rating'))

        if period == 'year':
            movies = movies.filter(release_date__year=today.year)
        elif period == 'month':
            movies = movies.filter(release_date__year=today.year, release_date__month=today.month)

        top_movies = movies.order_by('-avg_rating')[:self.number_of_top_movies]

        context.update({
            'top_movies': top_movies,
            'period': period,
        })

        return context