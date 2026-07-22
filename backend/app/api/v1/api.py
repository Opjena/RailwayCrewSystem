from fastapi import APIRouter

from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.user import router as users_router
from app.api.v1.endpoints.crew import router as crew_router
from app.api.v1.endpoints.cms import router as cms_router
from app.api.v1.endpoints.signon import router as signon_router
from app.api.v1.endpoints.main_data import router as main_data_router
from app.api.v1.endpoints.imports import router as imports_router
from app.api.v1.endpoints.audit import router as audit_router
from app.api.v1.endpoints.archive import router as archive_router

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
    cms_router,
    prefix="/cms",
    tags=["CMS Data"],
)

api_router.include_router(
    signon_router,
    prefix="/signon",
    tags=["Sign On/Off"],
)

api_router.include_router(
    main_data_router,
    prefix="/main-data",
    tags=["Main Data"],
)

api_router.include_router(
    imports_router,
    tags=["Excel Import"],
)

api_router.include_router(
    audit_router,
    tags=["Audit Logs"],
)

api_router.include_router(
    archive_router,
    prefix="/archive",
    tags=["Archive"],
)
