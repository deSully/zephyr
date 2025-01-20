import sqlite3
import pandas as pd
from sklearn.linear_model import LinearRegression
import os

class ModelTrainer:
    def __init__(self, db_path, results_path):
        self.db_path = db_path
        self.results_path = results_path

    def train_and_save_model(self):
        # Connexion à la base de données
        conn = sqlite3.connect(self.db_path)
        query = "SELECT * FROM api_metrics"
        df = pd.read_sql(query, conn)
        conn.close()

        # Grouper par service et endpoint pour l'entraînement de modèles distincts
        grouped = df.groupby(["service_name", "api_name"])

        for (service_name, api_name), group in grouped:
            # Entraîner un modèle par service + endpoint
            self.train_for_endpoint(service_name, api_name, group)

    def train_for_endpoint(self, service_name, api_name, group):
        # Préparer les données pour la régression linéaire
        X = group[["value"]]  # Variable indépendante (ex : valeur des métriques)
        y = group["timestamp"]  # Variable dépendante (ex : temps)

        # Entraîner un modèle de régression linéaire
        model = LinearRegression()
        model.fit(X, y)

        # Sauvegarder les résultats du modèle pour ce service et ce endpoint
        self.save_model_results(service_name, api_name, model)

    def save_model_results(self, service_name, api_name, model):
        # Définir le chemin de sauvegarde des résultats
        results_file = os.path.join(self.results_path, f"{service_name}-{api_name}-model.txt")
        with open(results_file, "w") as f:
            f.write(f"Model coefficients for {service_name} - {api_name}:\n")
            f.write(f"Coefficients: {model.coef_}\n")
            f.write(f"Intercept: {model.intercept_}\n")

        print(f"Model for {service_name} - {api_name} trained and saved to {results_file}")
