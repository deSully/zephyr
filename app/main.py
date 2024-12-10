# app/main.py

from fastapi import FastAPI
from app.controllers.metrics import router as metrics_router

app = FastAPI()

app.include_router(metrics_router)
