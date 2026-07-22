from fastapi import APIRouter

from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.user import router as users_router
from app.api.v1.endpoints.crew import router as crew_router
from app.api.v1.endpoints.cms_data import router as cms_router
from app.api.v1.endpoints.signon import router as signon_router
from app.api.v1.endpoints.main import router as main_router
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
    tags=["CMS Data"],
)

api_router.include_router(
    signon_router,
    tags=["Sign On"],
)

api_router.include_router(
    main_router,
    tags=["Main Data / Dashboard"],
)

api_router.include_router(
    archive_router,
    tags=["Archive"],
)

