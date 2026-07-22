"""Extended RCMS backend entrypoint.

This file is maintained for development reference. All production routes
are registered in main.py via app/api/v1/api.py.

Run (example):
  uvicorn app.main:app --reload
"""

from fastapi import FastAPI

app = FastAPI(title="Railway Crew Management System API (Extended)", version="1.0.0")


@app.get("/")
def root():
    return {"message": "Use app.main:app for the production entrypoint."}


