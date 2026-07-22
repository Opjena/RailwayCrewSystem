from fastapi import FastAPI
from sqlalchemy import text

from app.api.v1.api import api_router
from app.db.database import engine

app = FastAPI(
    title="Railway Crew Management System API",
    version="1.0.0"
)

# Register all API routes
app.include_router(
    api_router,
    prefix="/api/v1"
)

@app.get("/")
def root():
    return {
        "message": "Railway Crew Management System API"
    }

@app.get("/health")
def health():
    return {
        "status": "ok"
    }

    