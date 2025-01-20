#!/bin/bash

# Vérifier si le fichier de configuration est monté
if [ ! -f /app/config/config.yml ]; then
  echo "Erreur : Le fichier de configuration config.yml est manquant dans /app/config."
  exit 1
fi

# Initialiser la base de données si nécessaire
if [ ! -f /app/data/metrics.db ]; then
  echo "Initialisation de la base de données..."
  sqlite3 /app/data/metrics.db < /app/init_db.sql
fi

# Lancer l'application FastAPI et le JobManager
echo "Démarrage de l'application et du gestionnaire de tâches..."
exec python main.py
