# Installation Guide - Plotwist

## Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- git

## Installation from GitHub

### 1. Clone the repository
```bash
git clone https://github.com/RaffaeleAndrei32/Plotwist
cd plotwist
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure the database
```bash
python manage.py migrate
```

### 5. Create a superuser (admin)
```bash
python manage.py createsuperuser
```

### 6. Load sample data (optional)
```bash
python manage.py loaddata apps/movies/fixtures/genres.json
python manage.py loaddata apps/movies/fixtures/actors.json
python manage.py loaddata apps/movies/fixtures/director_films.json
```

### 7. Start the development server
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000`

---

## Initial Configuration

### Configuration Files

Main settings are located in `config/settings.py`. Modify according to your needs for production environments.

---

## Project Structure

```
plotwist/
├── apps/
│   ├── movies/          # Movie catalog management
│   ├── reviews/         # Review and rating system
│   ├── recommendations/ # Recommendation engine
│   └── users/           # User management
├── config/              # Django configuration
├── templates/           # Global HTML templates
├── static/              # CSS and JavaScript files
├── media/               # Media files (movie posters, profile images)
├── manage.py            # Django management script
└── requirements.txt     # Python dependencies
```

---

## Useful Commands

```bash
# Run tests
python manage.py test

# Create database migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

---

## Troubleshooting

### Error: "No module named 'django'"
Make sure you have activated the virtual environment and installed dependencies:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Database Error
If you encounter database issues, you can recreate it:
```bash
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Port 8000 Already in Use
Specify a different port:
```bash
python manage.py runserver 8001
```
