# app/main.py

from fastapi import FastAPI
from app.routers.metrics import metrics_router
from app.routers.health import health_router

app = FastAPI()

app.include_router(metrics_router, prefix="/api", tags=["Metrics"])
app.include_router(health_router, prefix="/api", tags=["Health"])
