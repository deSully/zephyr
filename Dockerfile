# Utiliser l'image officielle Python 3.12
FROM python:3.12-slim

# Installer les dépendances nécessaires, y compris sqlite3 et cron
RUN apt-get update && apt-get install -y sqlite3 cron

# Créer un répertoire pour l'application
WORKDIR /app

# Copier tous les fichiers du projet dans le conteneur
COPY . /app

# Créer un répertoire pour stocker les données de métriques (base de données SQLite)
RUN mkdir -p /app/data

# Définir le volume pour le stockage de la base de données SQLite
VOLUME ["/app/data"]

# Copier le script d'initialisation de la base de données
COPY init_db.sql /app/init_db.sql

# Copier le script d'entrypoint
COPY entrypoint.sh /entrypoint.sh

# Rendre le script d'entrypoint exécutable
RUN chmod +x /entrypoint.sh

# Installer les dépendances Python
RUN pip install -r requirements.txt

# Copier le fichier de configuration Cron
COPY crontab_config /etc/cron.d/train-cron

# Donner les bonnes permissions au fichier Cron
RUN chmod 0644 /etc/cron.d/train-cron

# Appliquer la configuration Cron
RUN crontab /etc/cron.d/crontab_config

# Exposer le port 8097 pour FastAPI
EXPOSE 8097

# Définir l'entrypoint pour exécuter le script d'initialisation et démarrer l'application
ENTRYPOINT ["/entrypoint.sh"]

# Démarrer cron en arrière-plan
CMD ["cron", "-f"]
