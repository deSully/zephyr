import requests
from faker import Faker
from random import randint, uniform
from datetime import datetime

# URL de l'API
API_URL = "http://localhost:8097/api/metrics/"

# Fonction pour générer des métriques factices
def generate_fake_metrics():
    fake = Faker()
    metrics = []

    # Création de 5 métriques par itération
    for _ in range(5):
        metric_type = fake.random_element(elements=("latency", "execution_time", "error_rate", "throughput"))
        value = 0.0
        if metric_type == "latency":
            value = uniform(50.0, 200.0)  # Latence entre 50ms et 200ms
        elif metric_type == "execution_time":
            value = uniform(0.1, 5.0)  # Temps d'exécution entre 0.1 et 5 secondes
        elif metric_type == "error_rate":
            value = randint(0, 5)  # Taux d'erreur entre 0 et 5 %
        elif metric_type == "throughput":
            value = randint(100, 1000)  # Nombre de requêtes par seconde

        metrics.append({
            "metric_type": metric_type,
            "value": value,
            "timestamp": fake.iso8601()
        })

    return metrics

# Fonction pour envoyer des données à l'API
def send_data_to_api(service_name, operation_name, metrics):
    data = {
        "name": operation_name,
        "service_name": service_name,
        "metrics": metrics
    }

    # Envoi de la requête POST à l'API
    response = requests.post(API_URL, json=data)

    if response.status_code == 200:
        print(f"Data for service '{service_name}' and operation '{operation_name}' sent successfully!")
    else:
        print(f"Failed to send data. Status code: {response.status_code}")

# Services et opérations à simuler
services = ["auth_service", "payment_service", "user_service"]
operations = ["login", "process_payment", "get_user_data", "register_user", "logout"]

# Envoi des données pour 3 services différents et générer 500 métriques
metric_count = 0
for service in services:
    for operation in operations:
        while metric_count < 500:
            fake_metrics = generate_fake_metrics()
            send_data_to_api(service, operation, fake_metrics)
            metric_count += len(fake_metrics)
            if metric_count >= 500:
                break
