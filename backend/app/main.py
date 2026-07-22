import logging

from fastapi import FastAPI
from sqlalchemy import text

from app.api.v1.api import api_router
from app.db.database import engine
from app.middleware.logging_middleware import RequestLoggingMiddleware

# ── structured logging ──────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

app = FastAPI(
    title="Railway Crew Management System API",
    version="1.0.0"
)

# ── middleware (order matters — logging first) ──────────────────────
app.add_middleware(RequestLoggingMiddleware)

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

@app.get("/db-test")
def db_test():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {
            "database": "Connected Successfully"
        }
    except Exception as e:
        return {
            "database": "Connection Failed",
            "error": str(e)
        }