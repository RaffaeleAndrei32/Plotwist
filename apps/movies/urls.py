from django.urls import path
from .views import *



app_name = 'movies'



urlpatterns = [
    path("", MovieListView.as_view(), name="list_movies"),
    path("<int:pk>/", MovieDetailView.as_view(), name="movie_info"),
    path("add_movie/", MovieCreateView.as_view(), name="add_movie"),
    path("watchlist/", WatchlistView.as_view(), name="watchlist"),
    path("my_movies/", UserMoviesListView.as_view(), name="user_movies"),
    path("<int:pk>/add_to_watchlist/", AddToWatchlistView.as_view(), name="add_to_watchlist"),
    path("<int:pk>/remove_from_watchlist/", RemoveFromWatchlistView.as_view(), name="remove_from_watchlist"),
    path("<int:pk>/edit/", MovieUpdateView.as_view(), name="edit_movie"),
    path("<int:pk>/delete/", DeleteMovieView.as_view(), name="delete_movie"),
]