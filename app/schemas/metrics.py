from pydantic import BaseModel
from typing import Optional

class MetricData(BaseModel):
    metric_type: str
    value: float
    timestamp: Optional[str] = None

class OperationCreate(BaseModel):
    name: str
    service_name: str
    metrics: Optional[list[MetricData]] = None
