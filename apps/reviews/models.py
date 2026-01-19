from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings


class Review(models.Model):
    title = models.CharField(
        max_length=200,
        help_text="Review title"
    )
    
    text = models.TextField(
        help_text="Review content"
    )
    
    rating = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ],
        help_text="Rating from 1 to 10"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    
    movie = models.ForeignKey(
        'movies.Movie',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    
    class Meta:
        app_label = 'reviews'
        ordering = ['-created_at']
        unique_together = ['user', 'movie']
    
    def __str__(self):
        return f"{self.user.username} - {self.movie.title} ({self.rating}/10)"

    @property
    def likes_count(self) -> int:
        return self.likes.count()


class ReviewLike(models.Model):
    """Tracks which users liked which reviews."""

    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='review_likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'reviews'
        unique_together = ['review', 'user']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} liked review {self.review_id}"
