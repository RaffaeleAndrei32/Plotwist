from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg, Q

from apps.movies.models import Movie


class RecommendationsListView(LoginRequiredMixin, ListView):
    """
    Content-Based Filtering Recommendations:
    Recommends movies based on genres, directors, and actors 
    from movies the user rated highly (7+).
    """
    model = Movie
    template_name = 'recommendations/recommendations_list.html'
    context_object_name = 'recommendations'
    paginate_by = 9
    login_url = 'accounts:login'

    def get_queryset(self):
        user = self.request.user
        
        # Get movies user has rated 7+
        liked_movies = Movie.objects.filter(
            reviews__user=user,
            reviews__rating__gte=7
        ).distinct()

        # If user hasn't rated any movies, return empty
        if not liked_movies.exists():
            return Movie.objects.none()

        # Extract preferred genres, directors, and actors
        preferred_genres = liked_movies.values_list('genres', flat=True).distinct()
        preferred_directors = liked_movies.values_list('director', flat=True).distinct()
        preferred_actors = liked_movies.values_list('actors', flat=True).distinct()

        # Find movies with similar characteristics
        # but exclude movies the user has already reviewed
        user_reviewed_movies = Movie.objects.filter(
            reviews__user=user
        ).values_list('id', flat=True)

        recommendations = Movie.objects.filter(
            Q(genres__in=preferred_genres) |
            Q(director__in=preferred_directors) |
            Q(actors__in=preferred_actors)
        ).exclude(
            id__in=user_reviewed_movies
        ).annotate(
            avg_rating=Avg('reviews__rating')
        ).distinct().order_by('-avg_rating')

        return recommendations

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Get user's liked movies count for context
        liked_count = Movie.objects.filter(
            reviews__user=user,
            reviews__rating__gte=7
        ).count()

        context.update({
            'liked_movies_count': liked_count,
        })

        return context
