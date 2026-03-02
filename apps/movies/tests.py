from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from decimal import Decimal

from apps.movies.models import Movie, Director, Genre, Actor
from apps.reviews.models import Review



User = get_user_model()



class MovieAverageRatingTestCase(TestCase):
    """Test Movie.get_average_rating() function."""
    
    def setUp(self):
        """Set up test data."""
        self.director = Director.objects.create(
            name="Test",
            surname="Director",
            birth_date="1980-01-01"
        )

        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )

        self.movie = Movie.objects.create(
            title="Test Movie",
            release_date="2023-01-01",
            length=120,
            director=self.director,
            logged_by=self.user
        )
    

    def test_average_rating_no_reviews(self):
        """Test average rating when movie has no reviews."""
        avg = self.movie.get_average_rating()
        self.assertEqual(avg, 0, "Average should be 0 when no reviews exist")
    

    def test_average_rating_single_review(self):
        """Test average rating with a single review."""
        Review.objects.create(
            title="Great movie",
            text="Very good",
            rating=8,
            user=self.user,
            movie=self.movie
        )

        avg = self.movie.get_average_rating()
        self.assertEqual(avg, 8.0, "Average should equal single rating")
    

    def test_average_rating_multiple_reviews(self):
        """Test average rating with multiple reviews."""
        ratings = [7, 8, 9]
        for idx, rating in enumerate(ratings):
            user = User.objects.create_user(
                username=f"user{idx}",
                email=f"user{idx}@example.com",
                password="pass123"
            )

            Review.objects.create(
                title=f"Review {idx}",
                text="Good",
                rating=rating,
                user=user,
                movie=self.movie
            )

        avg = self.movie.get_average_rating()
        expected = Decimal("8.0")
        self.assertEqual(avg, float(expected), "Average should be (7+8+9)/3 = 8.0")
    

    def test_average_rating_rounding(self):
        """Test that average rating is rounded to 1 decimal place."""
        ratings = [7, 8, 8]  # Average = 7.666...
        for idx, rating in enumerate(ratings):
            user = User.objects.create_user(
                username=f"rounduser{idx}",
                email=f"round{idx}@example.com",
                password="pass123"
            )
            Review.objects.create(
                title=f"Review {idx}",
                text="Test",
                rating=rating,
                user=user,
                movie=self.movie
            )

        avg = self.movie.get_average_rating()
        self.assertEqual(avg, 7.7, "Average should be rounded to 1 decimal")
    

    def test_average_rating_extreme_values(self):
        """Test average with extreme rating values (1 and 10)."""
        Review.objects.create(
            title="Bad",
            text="Terrible",
            rating=1,
            user=self.user,
            movie=self.movie
        )

        user2 = User.objects.create_user(
            username="user2",
            email="user2@example.com",
            password="pass123"
        )

        Review.objects.create(
            title="Great",
            text="Excellent",
            rating=10,
            user=user2,
            movie=self.movie
        )

        avg = self.movie.get_average_rating()
        self.assertEqual(avg, 5.5, "Average of 1 and 10 should be 5.5")



class MovieDetailViewTestCase(TestCase):
    """Test MovieDetailView via HTTP Client."""
    
    def setUp(self):
        """Set up test data."""
        self.client = Client()

        self.director = Director.objects.create(
            name="Steven",
            surname="Spielberg",
            birth_date="1946-12-18"
        )

        self.genre = Genre.objects.create(name="Sci-Fi")

        self.actor = Actor.objects.create(
            name="Tom",
            surname="Hanks",
            birth_date="1956-07-09"
        )
        
        self.user = User.objects.create_user(
            username="filmmaker",
            email="filmmaker@example.com",
            password="password123"
        )
        
        self.movie = Movie.objects.create(
            title="Inception",
            release_date="2010-07-16",
            length=148,
            director=self.director,
            logged_by=self.user,
            plot="A skilled thief who steals corporate secrets..."
        )

        self.movie.genres.add(self.genre)

        self.movie.actors.add(self.actor)
        
        # Add a review
        self.review_user = User.objects.create_user(
            username="reviewer",
            email="reviewer@example.com",
            password="password123"
        )
        
        self.review = Review.objects.create(
            title="Amazing Movie",
            text="One of the best movies ever made!",
            rating=9,
            user=self.review_user,
            movie=self.movie
        )
        
        self.url = reverse('movies:movie_info', kwargs={'pk': self.movie.pk})
    
    
    def test_movie_detail_view_returns_200(self):
        """Test that movie detail page returns HTTP 200."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200, "Page should return 200 OK")
    

    def test_movie_detail_view_uses_correct_template(self):
        """Test that correct template is used."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'movies/movie_info.html')
    

    def test_movie_detail_contains_movie_data(self):
        """Test that movie data is in response."""
        response = self.client.get(self.url)
        content = response.content.decode()
  
        self.assertIn("Inception", content, "Movie title should be in page")
        self.assertIn("148", content, "Movie length should be in page")
        self.assertIn("Steven", content, "Director name should be in page")
        self.assertIn("Sci-Fi", content, "Genre should be in page")
        self.assertIn("Tom Hanks", content, "Actor name should be in page")
    

    def test_movie_detail_contains_reviews(self):
        """Test that reviews are displayed."""
        response = self.client.get(self.url)
        content = response.content.decode()
        
        self.assertIn("Amazing Movie", content, "Review title should be in page")
        self.assertIn("One of the best movies", content, "Review text should be in page")
        self.assertIn("reviewer", content, "Reviewer username should be in page")
    

    def test_movie_detail_context_data(self):
        """Test that context data is correctly passed."""
        response = self.client.get(self.url)
        
        self.assertIn('movie', response.context)
        self.assertEqual(response.context['movie'].pk, self.movie.pk)
        self.assertIn('reviews', response.context)
        self.assertEqual(len(response.context['reviews']), 1)
    

    def test_movie_detail_unauthenticated_user(self):
        """Test page for unauthenticated user."""
        response = self.client.get(self.url)
        content = response.content.decode()
        
        # Should not show Edit Movie button
        self.assertNotIn("Edit Movie", content, "Edit button should not appear for guest")
        # Should not show in_watchlist
        self.assertFalse(response.context.get('in_watchlist', False))
        # Should not show user_added_movie
        self.assertFalse(response.context.get('user_added_movie', False))
    

    def test_movie_detail_authenticated_not_owner(self):
        """Test page for authenticated user who didn't add movie."""
        other_user = User.objects.create_user(
            username="otheruser",
            email="other@example.com",
            password="password123"
        )
        self.client.login(username="otheruser", password="password123")
        response = self.client.get(self.url)
        content = response.content.decode()
        
        # Should not show Edit button (not owner)
        self.assertNotIn("Edit Movie", content)
        self.assertFalse(response.context.get('user_can_edit', False))
    
    
    def test_movie_detail_authenticated_owner(self):
        """Test page for authenticated user who added movie."""
        self.client.login(username="filmmaker", password="password123")
        response = self.client.get(self.url)
        content = response.content.decode()
        
        # Should show Edit button (is owner)
        self.assertIn("Edit Movie", content)
        self.assertTrue(response.context.get('user_can_edit', False))
        self.assertTrue(response.context.get('user_added_movie', False))
    

    def test_movie_detail_average_rating_displayed(self):
        """Test that average rating is displayed."""
        response = self.client.get(self.url)
        content = response.content.decode()
        
        # Average of single 9-rating review
        self.assertIn("9/10", content, "Average rating should be displayed")
    

    def test_movie_detail_watchlist_button_authenticated(self):
        """Test watchlist button for authenticated user."""
        self.client.login(username="reviewer", password="password123")
        response = self.client.get(self.url)
        content = response.content.decode()
        
        # Should show Add to Watchlist
        self.assertIn("Add to Watchlist", content)
        self.assertFalse(response.context.get('in_watchlist', False))
    

    def test_movie_detail_404_nonexistent_movie(self):
        """Test that nonexistent movie returns 404."""
        url = reverse('movies:movie_info', kwargs={'pk': 9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404, "Nonexistent movie should return 404")
