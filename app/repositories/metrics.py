from app.models import db
from app.schemas.metrics import  MetricData
from typing import Optional

class MetricsRepository:
    def create_service(self, service_name: str):
        """Create a new service if it does not exist"""
        query = "INSERT OR IGNORE INTO services (name) VALUES (?)"
        db.execute(query, (service_name,))
        db.commit()

    def get_service_id(self, service_name: str):
        """Get the ID of a service by its name"""
        query = "SELECT id FROM services WHERE name = ?"
        result = db.execute(query, (service_name,)).fetchone()
        return result[0] if result else None

    def create_operation(self, service_id: int, operation_name: str):
        """Create a new operation if it does not exist"""
        query = "INSERT OR IGNORE INTO operations (service_id, name) VALUES (?, ?)"
        db.execute(query, (service_id, operation_name))
        db.commit()

    def get_operation_id(self, service_id: int, operation_name: str):
        """Get the ID of an operation by its name and service ID"""
        query = "SELECT id FROM operations WHERE service_id = ? AND name = ?"
        result = db.execute(query, (service_id, operation_name)).fetchone()
        return result[0] if result else None

    def insert_metric(self, operation_id: int, metric: MetricData):
        query = "INSERT INTO api_metrics (operation_id, metric_type, value, timestamp) VALUES (?, ?, ?, ?)"
        db.execute(query, (operation_id, metric.metric_type, metric.value, metric.timestamp))
        db.commit()

    def get_metrics(self, operation_name: Optional[str] = None, service_name: Optional[str] = None):
        # Définir la requête de base avec une jointure entre les tables
        query = """
            SELECT am.id, am.operation_id, am.metric_type, am.value, am.timestamp, 
                   o.name AS operation_name, s.name AS service_name
            FROM api_metrics am
            JOIN operations o ON am.operation_id = o.id
            JOIN services s ON o.service_id = s.id
            WHERE 1=1
        """

        # Ajouter des filtres à la requête si les paramètres sont fournis
        if operation_name:
            query += f" AND o.name = '{operation_name}'"
        if service_name:
            query += f" AND s.name = '{service_name}'"

        # Effectuer la requête et retourner les résultats
        results = db.execute(query)  # Exécution de la requête dans la base de données
        rows = results.fetchall()

        print(rows)

        # Structurer les données par service -> opérations -> métriques
        grouped_metrics = {}
        for row in rows:
            service = row[0]
            operation = row[1]
            metric = {
                "metric_type": row[2],
                "value": row[3],
                "timestamp": format_timestamp(row[4]),
            }

            # Organisation hiérarchique des données
            if service not in grouped_metrics:
                grouped_metrics[service] = {}
            if operation not in grouped_metrics[service]:
                grouped_metrics[service][operation] = []
            grouped_metrics[service][operation].append(metric)

        return grouped_metrics

def format_timestamp(timestamp: str):
    """Format the timestamp to a more readable format"""
    return timestamp.split("T")[0] + " " + timestamp.split("T")[1].split(".")[0]

