from fastapi import APIRouter

from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.user import router as users_router
from app.api.v1.endpoints.crew import router as crew_router
from app.api.v1.endpoints.schedule import router as schedule_router
from app.api.v1.endpoints.dashboard import router as dashboard_router
from app.api.v1.endpoints.reports import router as reports_router
from app.api.v1.endpoints.setting import router as settings_router
from app.api.v1.endpoints.lobby import router as lobby_router
from app.api.v1.endpoints.train import router as train_router
from app.api.v1.endpoints.duty import router as duty_router
from app.api.v1.endpoints.imports import router as imports_router
from app.api.v1.endpoints.audit import router as audit_router

api_router = APIRouter()

api_router.include_router(
    auth_router,
    prefix="/auth",
    tags=["Authentication"],
)

api_router.include_router(
    users_router,
    tags=["Users"],
)

api_router.include_router(
    crew_router,
    tags=["Crew Management"],
)

api_router.include_router(
    schedule_router,
    tags=["Schedule & Assignments"],
)

api_router.include_router(
    dashboard_router,
    tags=["Dashboard & Analytics"],
)

api_router.include_router(
    reports_router,
    tags=["Reports"],
)

api_router.include_router(
    settings_router,
    tags=["Settings"],
)

api_router.include_router(
    lobby_router,
    tags=["Lobby"],
)

api_router.include_router(
    train_router,
    tags=["Train"],
)

api_router.include_router(
    duty_router,
    tags=["Duty"],
)

api_router.include_router(
    imports_router,
    tags=["Excel Import"],
)

api_router.include_router(
    audit_router,
    tags=["Audit Logs"],
)
