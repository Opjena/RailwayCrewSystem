from fastapi import APIRouter

from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.user import router as users_router
from app.api.v1.endpoints.crew import router as crew_router
from app.api.v1.endpoints.schedule import router as schedule_router
from app.api.v1.endpoints.dashboard import router as dashboard_router
from app.api.v1.endpoints.reports import router as reports_router
from app.api.v1.endpoints.setting import router as settings_router

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
