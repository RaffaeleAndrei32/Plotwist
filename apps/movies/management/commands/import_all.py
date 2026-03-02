import os
import json
import requests
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.conf import settings
from django.contrib.auth import get_user_model
from apps.movies.models import Movie, Director, Genre, Actor

User = get_user_model()

class Command(BaseCommand):
    help = 'Populates the database from JSON fixtures and downloads posters from TMDB'

    API_KEY = settings.TMDB_API_KEY
    FIXTURES_DIR = os.path.join(settings.BASE_DIR, "apps", "movies", "fixtures")
    LANGUAGE = "en-US"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('--- Starting Global Import ---'))
        
        if not self.import_genres(): return
        if not self.import_directors(): return
        if not self.import_actors(): return
        if not self.import_movies(): return
        
        self.stdout.write(self.style.SUCCESS('\n=== ALL IMPORTS COMPLETED ==='))

    def get_tmdb_poster_url(self, movie_title):
        search_url = "https://api.themoviedb.org/3/search/movie"
        params = {"api_key": self.API_KEY, "query": movie_title, "language": self.LANGUAGE}
        try:
            response = requests.get(search_url, params=params, timeout=5)
            data = response.json()
            if data.get("results"):
                path = data["results"][0].get("poster_path")
                return f"https://image.tmdb.org/t/p/w500{path}" if path else None
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"  ⚠ TMDB Error for {movie_title}: {e}"))
        return None

    def import_genres(self):
        self.stdout.write("\n> Importing Genres...")
        file_path = os.path.join(self.FIXTURES_DIR, 'genres.json')
        with open(file_path, 'r') as f:
            for item in json.load(f):
                Genre.objects.get_or_create(name=item['name'])
        return True

    def import_directors(self):
        self.stdout.write("> Importing Directors...")
        file_path = os.path.join(self.FIXTURES_DIR, 'director_films.json')
        with open(file_path, 'r') as f:
            for data in json.load(f):
                Director.objects.update_or_create(
                    name=data['name'], 
                    surname=data['surname'],
                    defaults={'birth_date': data.get('birth_date')}
                )
        return True

    def import_actors(self):
        self.stdout.write("> Importing Actors...")
        file_path = os.path.join(self.FIXTURES_DIR, 'actors.json')
        with open(file_path, 'r') as f:
            for data in json.load(f):
                Actor.objects.update_or_create(
                    name=data['name'], 
                    surname=data['surname'],
                    defaults={'birth_date': data.get('birth_date')}
                )
        return True

    def import_movies(self):
        self.stdout.write("> Importing Movies & Posters...")
        file_path = os.path.join(self.FIXTURES_DIR, 'movies_with_posters.json')
        admin_user = User.objects.filter(is_staff=True).first()

        if not admin_user:
            self.stdout.write(self.style.ERROR("No admin user found."))
            return False

        with open(file_path, 'r') as f:
            movies_data = json.load(f)

        for data in movies_data:
            movie, created = Movie.objects.get_or_create(
                title=data['title'],
                defaults={
                    'director': Director.objects.get(id=data['director_id']),
                    'release_date': data['release_date'],
                    'length': data['length'],
                    'logged_by': admin_user,
                    'plot': data.get('plot', '')
                }
            )

            if created:
                movie.genres.set(Genre.objects.filter(id__in=data['genres']))
                movie.actors.set(Actor.objects.filter(id__in=data['actors']))

                if not movie.poster:
                    poster_url = self.get_tmdb_poster_url(movie.title)
                    if poster_url:
                        try:
                            resp = requests.get(poster_url)
                            file_name = f"{movie.title.replace(' ', '_')}.jpg"
                            movie.poster.save(file_name, ContentFile(resp.content), save=True)
                            self.stdout.write(f"  OK {movie.title} (Poster downloaded)")
                        except Exception:
                            self.stdout.write(f"  OK {movie.title} (Poster download failed)")
                else:
                    self.stdout.write(f"  OK {movie.title}")
            else:
                self.stdout.write(f"  ERROR {movie.title} already exists")
        return True