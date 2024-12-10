#!/bin/bash

# Initialiser la base de données SQLite
sqlite3 /app/db.sqlite3 < /app/init_db.sql

# Démarrer l'application FastAPI avec uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000