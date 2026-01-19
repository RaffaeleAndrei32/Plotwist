#!/usr/bin/env python
import os
import sys
import json
import django
import requests
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.movies.models import Movie, Director, Genre, Actor
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

directors_imported_count = 0

API_KEY = "2674f1f57c98c47e6bef9d9db85577dc"
SAVE_FOLDER = os.path.join("media", "movies", "posters")
FIXTURES_DIR = os.path.join("apps", "movies", "fixtures")
LANGUAGE = "en-US"

if not os.path.exists(SAVE_FOLDER):
    os.makedirs(SAVE_FOLDER)


def get_poster_path(movie_title):
    """Search movie on TMDB and return poster path."""
    search_url = "https://api.themoviedb.org/3/search/movie"
    params = {
        "api_key": API_KEY,
        "query": movie_title,
        "language": LANGUAGE
    }
    
    try:
        response = requests.get(search_url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        if data["results"]:
            poster_path = data["results"][0].get("poster_path")
            if poster_path:
                return f"https://image.tmdb.org/t/p/w500{poster_path}"
    except Exception as e:
        print(f"  ⚠ Error searching '{movie_title}': {e}")
    
    return None


def import_directors():
    """Import directors from JSON into DB."""
    print("\n" + "="*60)
    print("DIRECTORS IMPORT")
    print("="*60)
    
    file_path = os.path.join(FIXTURES_DIR, 'director_films.json')
    
    if not os.path.exists(file_path):
        print(f"✗ Error: File {file_path} not found.")
        return False

    print("Starting directors import...\n")

    with open(file_path, 'r', encoding='utf-8') as f:
        directors_data = json.load(f)

    created_count = 0
    skipped_count = 0

    for data in directors_data:
        director, created = Director.objects.get_or_create(
            name=data['name'],
            surname=data['surname'],
            defaults={'birth_date': data.get('birth_date')}
        )
        
        if created:
            print(f"✓ Created: {director.name} {director.surname}")
            created_count += 1
        else:
            if data.get('birth_date') and not director.birth_date:
                director.birth_date = data['birth_date']
                director.save()
                print(f"◆ Updated date: {director.name} {director.surname}")
            else:
                skipped_count += 1

    print(f"\n--- DIRECTORS SUMMARY ---")
    print(f"Directors created: {created_count}")
    print(f"Directors skipped: {skipped_count}")
    print(f"Import completed!\n")
    return True


def import_genres():
    """Import genres from JSON into DB."""
    print("\n" + "="*60)
    print("GENRES IMPORT")
    print("="*60)
    
    file_path = os.path.join(FIXTURES_DIR, 'genres.json')
    
    if not os.path.exists(file_path):
        print(f"✗ Error: File {file_path} not found.")
        return False

    print("Starting genres import...\n")

    with open(file_path, 'r', encoding='utf-8') as f:
        genres_data = json.load(f)

    created_count = 0
    skipped_count = 0

    for item in genres_data:
        genre, created = Genre.objects.get_or_create(name=item['name'])
        
        if created:
            print(f"✓ Added: {genre.name}")
            created_count += 1
        else:
            skipped_count += 1

    print(f"\n--- GENRES SUMMARY ---")
    print(f"Genres added: {created_count}")
    print(f"Genres already present: {skipped_count}")
    print(f"Import completed!\n")
    return True


def import_actors():
    """Import actors from JSON into DB."""
    print("\n" + "="*60)
    print("ACTORS IMPORT")
    print("="*60)
    
    file_path = os.path.join(FIXTURES_DIR, 'actors.json')
    
    if not os.path.exists(file_path):
        print(f"✗ Error: File {file_path} not found.")
        return False

    print("Starting actors import...\n")

    with open(file_path, 'r', encoding='utf-8') as f:
        actors_data = json.load(f)

    created_count = 0
    updated_count = 0
    skipped_count = 0

    for data in actors_data:
        actor, created = Actor.objects.get_or_create(
            name=data['name'],
            surname=data['surname'],
            defaults={'birth_date': data.get('birth_date')}
        )
        
        if created:
            print(f"✓ Created: {actor.name} {actor.surname}")
            created_count += 1
        else:
            if data.get('birth_date') and not actor.birth_date:
                actor.birth_date = data['birth_date']
                actor.save()
                print(f"◆ Updated date: {actor.name} {actor.surname}")
                updated_count += 1
            else:
                skipped_count += 1

    print(f"\n--- ACTORS SUMMARY ---")
    print(f"Actors created: {created_count}")
    print(f"Actors updated: {updated_count}")
    print(f"Actors skipped: {skipped_count}")
    print(f"Import completed!\n")
    return True


def import_movies():
    """Import movies from JSON into DB."""
    print("\n" + "="*60)
    print("MOVIES IMPORT")
    print("="*60)
    
    file_path = os.path.join(FIXTURES_DIR, 'movies_with_posters.json')
    
    if not os.path.exists(file_path):
        print(f"✗ Error: File {file_path} not found.")
        return False

    with open(file_path, 'r', encoding='utf-8') as f:
        movies_data = json.load(f)

    # Get first admin user for logged_by
    admin_user = CustomUser.objects.filter(is_staff=True).first()
    if not admin_user:
        print("✗ Error: No admin user found in DB.")
        return False

    print(f"Using admin user: {admin_user.username}")
    print(f"Starting import of {len(movies_data)} movies...\n")

    created_count = 0
    skipped_count = 0

    for data in movies_data:
        try:
            # Check if movie already exists
            if Movie.objects.filter(title=data['title']).exists():
                print(f"⊘ Skipped (exists): {data['title']}")
                skipped_count += 1
                continue

            # Get director
            director = Director.objects.get(id=data['director_id'])

            # Create movie
            movie = Movie.objects.create(
                title=data['title'],
                director=director,
                release_date=data['release_date'],
                length=data['length'],
                logged_by=admin_user,
                plot=data.get('plot', '')
            )

            # Add genres
            genres = Genre.objects.filter(id__in=data['genres'])
            movie.genres.set(genres)

            # Add actors
            if data['actors']:
                actors = Actor.objects.filter(id__in=data['actors'])
                movie.actors.set(actors)

            # Add poster if exists
            if data['poster']:
                poster_path = os.path.join("movies", "posters", data['poster'])
                full_poster_path = os.path.join('media', poster_path)
                
                if os.path.exists(full_poster_path):
                    movie.poster = poster_path
                    movie.save()
                    print(f"✓ Created with poster: {movie.title}")
                else:
                    print(f"✓ Created (poster not found): {movie.title}")
            else:
                print(f"✓ Created: {movie.title}")

            created_count += 1

        except Director.DoesNotExist:
            print(f"✗ Error: Director not found for {data['title']}")
        except Exception as e:
            print(f"✗ Error creating {data['title']}: {e}")

    print(f"\n--- MOVIES SUMMARY ---")
    print(f"Movies created: {created_count}")
    print(f"Movies skipped: {skipped_count}")
    print(f"Import completed!\n")
    return True


def download_posters():
    """Download posters from TMDB for movies in JSON."""
    print("\n" + "="*60)
    print("DOWNLOADING POSTERS FROM TMDB")
    print("="*60)
    
    file_path = os.path.join(FIXTURES_DIR, 'director_films.json')
    
    if not os.path.exists(file_path):
        print(f"✗ Error: File {file_path} not found.")
        return False

    with open(file_path, "r", encoding="utf-8") as f:
        directors_data = json.load(f)

    print(f"Starting poster download...\n")

    downloaded_count = 0
    not_found_count = 0
    error_count = 0

    for entry in directors_data:
        director_name = f"{entry['name']} {entry['surname']}"
        print(f"--- Movies by: {director_name} ---")
        
        for film in entry["films"]:
            print(f"Searching poster for: {film}...", end=" ")
            poster_url = get_poster_path(film)
            
            if poster_url:
                try:
                    img_data = requests.get(poster_url, timeout=5).content
                    clean_name = "".join(c for c in film if c.isalnum() or c in (' ', '_')).rstrip()
                    file_path = os.path.join(SAVE_FOLDER, f"{clean_name}.jpg")
                    
                    with open(file_path, "wb") as handler:
                        handler.write(img_data)
                    print("✓ OK")
                    downloaded_count += 1
                except Exception as e:
                    print(f"✗ DOWNLOAD ERROR: {e}")
                    error_count += 1
            else:
                print("⊘ NOT FOUND")
                not_found_count += 1

    print(f"\n--- DOWNLOAD SUMMARY ---")
    print(f"Posters downloaded: {downloaded_count}")
    print(f"Posters not found: {not_found_count}")
    print(f"Errors: {error_count}")
    print(f"Download completed!\n")
    return True


def show_menu():
    """Show interactive menu."""
    print("\n" + "="*60)
    print("PLOTWIST - IMPORT SCRIPT")
    print("="*60)
    print("\nChoose what to import:\n")
    print("  1. Import genres")
    print("  2. Import directors")
    print("  3. Import actors")
    print("  4. Import movies")
    print("  5. Download posters from TMDB")
    print("  6. Import EVERYTHING (genres → directors → actors → movies)")
    print("  0. Exit\n")


def main():
    """Main menu."""
    while True:
        show_menu()
        choice = input("Enter choice (0-6): ").strip()
        
        if choice == '0':
            print("\nGoodbye!\n")
            sys.exit(0)
        elif choice == '1':
            import_genres()
        elif choice == '2':
            import_directors()
        elif choice == '3':
            import_actors()
        elif choice == '4':
            import_movies()
        elif choice == '5':
            download_posters()
        elif choice == '6':
            print("\nFull import in progress...\n")
            if import_genres() and import_directors() and import_actors() and import_movies():
                print("✓ Import completed successfully!")
            else:
                print("✗ Import interrupted due to errors.")
        else:
            print("\n✗ Invalid choice. Try again.\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nImport cancelled by user.\n")
        sys.exit(1)
