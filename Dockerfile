# Usa un'immagine Python ufficiale e leggera
FROM python:3.12-slim

# Evita che Python generi file .pyc e assicura output in tempo reale
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Imposta la directory di lavoro nel container
WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    python3-dev \
    zlib1g-dev \
    libjpeg-dev \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Installa le dipendenze Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copia il resto del codice del progetto
COPY . /app/

# Comando di default (che sovrascriveremo nel docker-compose)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]