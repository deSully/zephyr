from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to Zephyr - Intelligent Cache Service"}

@app.get("/health")
def health_check():
    return {"status": "Zephyr is running"}
