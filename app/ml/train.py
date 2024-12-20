import sqlite3
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import joblib
import datetime

# Connexion à la base de données SQLite
def connect_db():
    return sqlite3.connect('/app/data/metrics.db')

# Récupérer les métriques et les grouper par service et opération
def get_metrics():
    conn = connect_db()
    query = """
    SELECT s.name AS service_name, o.name AS operation_name, m.metric_type, m.value, m.timestamp
    FROM api_metrics m
    JOIN operations o ON m.operation_id = o.id
    JOIN services s ON o.service_id = s.id
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Appliquer la régression pour chaque opération
def train_model(df):
    grouped = df.groupby(['service_name', 'operation_name'])

    for (service, operation), group in grouped:
        print(f"Entrainement pour {service} - {operation}...")

        # Séparer les variables d'entrée et la variable cible
        X = group[['timestamp']]  # Ici, tu peux ajouter d'autres features si nécessaire
        y = group['value']

        # Convertir le timestamp en format numérique (par exemple, en secondes depuis le début)
        X['timestamp'] = pd.to_datetime(X['timestamp']).astype(int) / 10**9  # Conversion en secondes

        # Séparer les données en train/test
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Appliquer le modèle de régression linéaire
        model = LinearRegression()
        model.fit(X_train, y_train)

        # Évaluer le modèle (optionnel)
        print(f"Score R^2 pour {service} - {operation}: {model.score(X_test, y_test)}")

        # Sauvegarder le modèle dans un fichier
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f"/app/models/{service}-{operation}-{timestamp}.pkl"
        joblib.dump(model, filename)
        print(f"Modèle sauvegardé sous {filename}")

# Fonction principale pour exécuter le processus
def main():
    df = get_metrics()  # Récupérer les données
    train_model(df)     # Entraîner et sauvegarder les modèles

if __name__ == '__main__':
    main()
