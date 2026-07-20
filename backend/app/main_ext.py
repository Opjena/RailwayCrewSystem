"""Extended RCMS backend entrypoint.

Constraint: do NOT modify existing files.

This file wires additional PRD modules (Lobby/Train/Duty/Import/Audit) via a separate
ASGI application.

Run (example):
  uvicorn app.main_ext:app --reload

Note: This requires the modules to be added under app/api/v1/endpoints/*.
"""

from fastapi import FastAPI

# Existing router wiring cannot be edited per constraint; this app only mounts
# newly added routers that you will create.

app = FastAPI(title="Railway Crew Management System API (Extended)", version="1.0.0")


@app.get("/")
def root():
    return {"message": "RCMS Extended API"}


# Routers are intentionally not imported here until the corresponding modules
# exist. When you add new endpoints, update this file accordingly.

