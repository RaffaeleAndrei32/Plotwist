from datetime import date

from django.db.models import Avg, Q
from django.views.generic import TemplateView

from apps.movies.models import Movie


class HomeView(TemplateView):
    """
    Dashboard View: Shows top rated movies and personalized recommendations
    (content-based filtering for authenticated users)
    """
    template_name = "home.html"
    number_of_top_movies = 9
    number_of_recommendations = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Top Rated Movies Section
        period = self.request.GET.get('period', 'all')
        today = date.today()

        movies = Movie.objects.annotate(avg_rating=Avg('reviews__rating'))

        if period == 'year':
            movies = movies.filter(release_date__year=today.year)
        elif period == 'month':
            movies = movies.filter(release_date__year=today.year, release_date__month=today.month)

        top_movies = movies.order_by('-avg_rating')[:self.number_of_top_movies]

        # Personalized Recommendations (Content-Based Filtering)
        recommendations = []
        if self.request.user.is_authenticated:
            # Get movies user has rated 7+
            liked_movies = Movie.objects.filter(
                reviews__user=self.request.user,
                reviews__rating__gte=7
            ).distinct()

            if liked_movies.exists():
                # Extract preferred genres, directors, and actors
                preferred_genres = liked_movies.values_list('genres', flat=True).distinct()
                preferred_directors = liked_movies.values_list('director', flat=True).distinct()
                preferred_actors = liked_movies.values_list('actors', flat=True).distinct()

                # Find movies with similar characteristics
                user_reviewed_movies = Movie.objects.filter(
                    reviews__user=self.request.user
                ).values_list('id', flat=True)

                recommendations = Movie.objects.filter(
                    Q(genres__in=preferred_genres) |
                    Q(director__in=preferred_directors) |
                    Q(actors__in=preferred_actors)
                ).exclude(
                    id__in=user_reviewed_movies
                ).annotate(
                    avg_rating=Avg('reviews__rating')
                ).distinct().order_by('-avg_rating')[:self.number_of_recommendations]

        context.update({
            'top_movies': top_movies,
            'recommendations': recommendations,
            'period': period,
            'has_recommendations': bool(recommendations),
        })

        return context