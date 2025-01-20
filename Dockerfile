# Utiliser l'image officielle Python 3.12
FROM python:3.12-slim

# Installer les dépendances nécessaires, y compris sqlite3
RUN apt-get update && apt-get install -y sqlite3 && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app

# Créer un répertoire pour stocker les données de métriques (base de données SQLite)
RUN mkdir -p /app/data

# Définir le volume pour le stockage de la base de données SQLite
VOLUME ["/app/data"]

# Définir le volume pour le fichier de configuration (config.yml)
VOLUME ["/app/config"]

COPY init_db.sql /app/init_db.sql

COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port 8097 pour FastAPI
EXPOSE 8097

ENTRYPOINT ["/entrypoint.sh"]
