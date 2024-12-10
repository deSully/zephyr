# Utiliser l'image officielle Python 3.12
FROM python:3.12-slim

# Installer les dépendances nécessaires, y compris sqlite3
RUN apt-get update && apt-get install -y sqlite3

# Créer un répertoire pour l'application
WORKDIR /app

# Copier tous les fichiers du projet dans le conteneur
COPY . /app

# Create a directory for storing metrics data (SQLite DB)
RUN mkdir -p /app/data

# Define the volume for SQLite database storage
VOLUME ["/app/data"]

# Copier le script d'initialisation de la base de données
COPY init_db.sql /app/init_db.sql

# Copier le script d'entrypoint
COPY entrypoint.sh /entrypoint.sh

# Rendre le script d'entrypoint exécutable
RUN chmod +x /entrypoint.sh

# Installer les dépendances Python
RUN pip install -r requirements.txt

# Définir l'entrypoint pour exécuter le script d'initialisation et démarrer l'application
ENTRYPOINT ["/entrypoint.sh"]

# Exposer le port 8000 pour FastAPI
EXPOSE 8000
