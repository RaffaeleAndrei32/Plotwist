from django.urls import path
from . import views



app_name = 'reviews'



urlpatterns = [
    path('', views.UserReviewsListView.as_view(), name='reviews_list'),
    path('add/<int:pk>/', views.AddReviewView.as_view(), name='add_review'),
    path('edit/<int:review_pk>/', views.EditReviewView.as_view(), name='edit_review'),
    path('delete/<int:review_pk>/', views.DeleteReviewView.as_view(), name='delete_review'),
    path('like/<int:review_pk>/', views.ToggleReviewLikeView.as_view(), name='toggle_like'),
]
