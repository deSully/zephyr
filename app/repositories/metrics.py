from app.models import db
from app.schemas.metrics import  MetricData

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
