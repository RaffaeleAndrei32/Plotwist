# Plotwist

Plotwist is a comprehensive web platform for movie logging, scoring, and reviewing. Built with a modern tech stack, it allows users to explore a catalog of movies, leave detailed reviews, and manage content through a robust role-based authentication system.

## Features

- **Movie Catalog:** Add, edit, and manage movies with rich details (director, actors, genres, plot, posters).
- **Reviews & Ratings:** Rate movies and write detailed reviews to share your opinion.
- **Role-Based Access Control (RBAC):**
  - *Standard Users:* Can browse, rate, and review movies.
  - *Moderators:* Can access the admin panel to manage movie entries and categories.
  - *Superusers:* Have full system control.
- **User System:** Secure authentication and profile customization.
- **Recommendations:** Personalized movie recommendations (coming soon).

## Tech Stack

- **Backend:** Django 6.0, Python 3.12
- **Database:** PostgreSQL 15 (Docker) / SQLite (Local Fallback)
- **Frontend:** HTML5, CSS3, Bootstrap 5 (via `crispy-bootstrap5`)
- **Infrastructure:** Docker & Docker Compose

---

## Quick Start (Docker - Recommended)

The application is fully containerized. The easiest and recommended way to run the project locally is by using Docker.

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/) & Docker Compose
- Git

### Installation Steps

**Clone the repository:**
```bash
git clone https://github.com/RaffaeleAndrei32/Plotwist.git
cd Plotwist
```

**Environment Variables:**
Create a .env and .env.docker file in the root directory to store your configurations (e.g., SECRET_KEY, database credentials, see .env.example and .env.docker.example)

**Build and start the cointainer:**
```bash

docker compose up --build -d

```

**Apply database migrations:**
```bash

docker compose exec web python manage.py migrate

```

---
### Installation Steps
This project provides two distinct ways to populate the database, depending on your goal.

**Option 1: Load Sample Data (Fixtures):**
Populate the empty PostgreSQL database with initial movies, genres, actors, and configured users.
```bash
docker compose exec web python manage.py loaddata apps/movies/fixtures/movies_backup.json
```
The application will now be running at http://localhost:8000.

**Option 2: Full Data Ingestion (ETL via TMDB API)**
The application includes a Django Management Command designed to fetch, parse, and ingest raw JSON data, while automatically downloading movie posters from the TMDB API.

Prerequisite: You must add your TMDB API key to the .env.docker file:
```bash
TMDB_API_KEY=your_api_key_here
```

Run the data ingestion pipeline:
```bash
docker compose exec web python manage.py import_all
```

Note: This command is idempotent. It uses update_or_create logic to safely update existing records without creating duplicates, and gracefully handles missing API responses or missing posters.

**Demo Credentials:**
If you loaded the sample data using the commands above, you can log in to the admin panel (http://localhost:8000/admin) using the following pre-configured account:

Moderator (Limited Admin Access):

    Username: moderator

    Password: moderator
---

## Local Development (Without Docker):
If you prefer to run the project locally using SQLite for quick prototyping, create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

**Install dependencies:**
```bash
pip install -r requirements.txt
```

**Run migrations and start the server**
```bash
python manage.py migrate
python manage.py runserver
```

---
## License

This project is licensed under the MIT License
