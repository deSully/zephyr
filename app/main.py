from fastapi import FastAPI
import asyncio
from app.scheduler import JobManager
app = FastAPI()

# Exemple de route
@app.get("/")
async def read_root():
    return {"message": "Application Zephyr running"}

# Lancer FastAPI et JobManager
def main():
    job_manager = JobManager("/app/config/config.yml")
    asyncio.create_task(job_manager.start_jobs())  # Exécution asynchrone des jobs
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8097)

if __name__ == "__main__":
    main()
