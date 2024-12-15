from idlelib.query import Query
from typing import Optional, List

from fastapi import APIRouter
from app.schemas.metrics import OperationCreate
from app.repositories.metrics import MetricsRepository
from schemas.metrics import MetricData

metrics_router = APIRouter()
repo = MetricsRepository()

@metrics_router.post("/metrics/")
async def create_metrics(data: OperationCreate):
    """Create a new operation and insert metrics"""
    repo.create_service(data.service_name)
    service_id = repo.get_service_id(data.service_name)

    # Create the operation
    repo.create_operation(service_id, data.name)
    operation_id = repo.get_operation_id(service_id, data.name)

    # Insert the metrics
    for metric in data.metrics:
        repo.insert_metric(operation_id, metric)

    return {"status": "success", "message": "Metrics added successfully"}

@metrics_router.get("/metrics/", response_model=List[MetricData])
async def get_metrics(
        operation_name: Optional[str] = Query(None, alias="operation_name", description="Filtrer par nom de l'opération"),
        service_name: Optional[str] = Query(None, alias="service_name", description="Filtrer par nom du service")
):
    # On va chercher les métriques en appliquant les filtres s'ils existent
    metrics = repo.get_metrics(operation_name=operation_name, service_name=service_name)
    return metrics