from django.urls import path
from . import views

app_name = 'recommendations'

urlpatterns = [
    path('', views.RecommendationsListView.as_view(), name='recommendations_list'),
]
