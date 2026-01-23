# Plotwist

Plotwist is a web platform for movies logging, scoring and reviewing.

## Quick Start

### Installation from GitHub

```bash
git clone https://github.com/yourusername/plotwist.git
cd plotwist
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Visit `http://127.0.0.1:8000` to access the application.

---

## Features

- 🎬 **Movie Catalog** - Add, edit, and manage movies with details (director, actors, genres, plot)
- ⭐ **Reviews & Ratings** - Rate movies and write detailed reviews
- 👥 **User System** - User authentication with profile customization
- 🎯 **Recommendations** - Personalized movie recommendations (coming soon)
- 📊 **Admin Dashboard** - Manage content with Django admin

---

## Tech Stack

- **Backend**: Django 6.0
- **Database**: SQLite3
- **Frontend**: Bootstrap 5 (via django-crispy-forms)
- **Python**: 3.9+

---

## Installation

For complete installation instructions, see [INSTALLATION.md](INSTALLATION.md).

---

## Project Structure

```
plotwist/
├── apps/              # Django applications
│   ├── movies/        # Movie catalog management
│   ├── reviews/       # Review and rating system
│   ├── recommendations/  # Recommendation engine
│   └── users/         # User authentication
├── config/            # Django configuration
├── templates/         # HTML templates
├── static/            # CSS, JavaScript, images
└── media/             # User uploads (posters, profiles)
```

---

## Development

Run tests:
```bash
python manage.py test
```

Load sample data:
```bash
python manage.py loaddata apps/movies/fixtures/genres.json
python manage.py loaddata apps/movies/fixtures/actors.json
```

---

## License

MIT License - see LICENSE file for details