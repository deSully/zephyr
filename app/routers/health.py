from fastapi import APIRouter

from app.repositories.health import HealthRepository

health_router = APIRouter()

@health_router.get("/health", summary="Health Check", description="Check the health of the service and database.")
async def health_check():
    repo = HealthRepository()
    try:
        # Check the health of the database
        db_status, stats = repo.get_health_status()

        # Return the health status
        return {
            "status": "healthy" if db_status else "degraded",
            "database_status": "available" if db_status else "unavailable",
            "stats": stats if db_status else "No stats available, database not ready."
        }
    except Exception as e:
        # Return an error if the health check fails
        return {
            "status": "unhealthy",
            "error": str(e)
        }
