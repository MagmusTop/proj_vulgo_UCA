    # Use the official Python runtime image
    FROM python:3.14.8-slim@sha256:a2b82f3c48559aa0a8446d9af49826b6e2b2016f4cd2afabfe6013ec53729170

    # Set environment variables 
    # Prevents Python from writing pyc files to disk
    ENV PYTHONDONTWRITEBYTECODE=1
    #Prevents Python from buffering stdout and stderr
    ENV PYTHONUNBUFFERED=1 

    # Utilisateur sans privilèges pour faire tourner l'application
    RUN useradd -m appuser

    # Set the working directory inside the container
    WORKDIR /app

    # Outils de compilation (inutiles si toutes vos dépendances ont une wheel)
    RUN apt-get update \
        && apt-get install -y --no-install-recommends build-essential \
        && rm -rf /var/lib/apt/lists/*
    RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

    # Les dépendances d'abord, pour profiter du cache de Docker
    COPY requirements.txt ./
    RUN pip install --no-cache-dir -r requirements.txt

    # Puis le code
    COPY . .
    RUN chown -R appuser:appuser /app
    USER appuser
    # Expose the Django port
    EXPOSE 8000
    
    # Run Django’s development server
    #CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


    # Remplacez config.wsgi:application par le chemin WSGI de votre projet
    CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]