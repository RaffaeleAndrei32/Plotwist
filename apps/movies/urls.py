from django.urls import path
from .views import *



app_name = 'movies'



urlpatterns = [
    path("", MovieListView.as_view(), name="list_movies"),
    path("add_movie/", MovieCreateView.as_view(), name="add_movie"),
]