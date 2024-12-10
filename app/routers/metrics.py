from fastapi import APIRouter
from app.schemas.metrics import OperationCreate
from app.repositories.metrics import MetricsRepository

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
