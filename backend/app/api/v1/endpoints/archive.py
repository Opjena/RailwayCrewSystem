from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.archive_data import ArchiveDataResponse
from app.schemas.common import APIResponse, PaginatedResponse
from app.services.archive_service import ArchiveService
from app.auth.permissions import require_admin, require_supervisor

router = APIRouter(
    prefix="/archive",
    tags=["Archive"],
)


@router.post("/main/{main_data_id}")
def archive_main_data(
    main_data_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    """
    Archive a MainData record.

    Business workflow (single transaction):
      1. Find MainData
      2. Create ArchiveData snapshot
      3. Soft-delete MainData
      4. Audit Log
    """
    service = ArchiveService(db, request)
    archive = service.archive_main_data(
        main_data_id, actor_username=current_user.username
    )
    return APIResponse(
        success=True,
        message="MainData archived successfully",
        data=ArchiveDataResponse.model_validate(archive).model_dump(),
    )


@router.get("")
def get_all_archive(
    request: Request,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=1000),
    crew_id: str | None = Query(None, description="Filter by crew ID"),
    search: str | None = Query(None, description="Keyword search"),
    sort: str = Query("id", description="Sort column"),
    order: str = Query("asc", description="Sort order (asc/desc)"),
    db: Session = Depends(get_db),
    current_user=Depends(require_supervisor),
):
    """Get all archived records with pagination, filtering, and search"""
    service = ArchiveService(db, request)
    result = service.get_all_archive(
        skip=skip,
        limit=limit,
        crew_id=crew_id,
        search=search,
        sort=sort,
        order=order,
    )
    return APIResponse(
        success=True,
        message="Archived records retrieved successfully",
        data=PaginatedResponse(
            items=[
                ArchiveDataResponse.model_validate(a).model_dump()
                for a in result["items"]
            ],
            total=result["total"],
            page=result["page"],
            page_size=result["page_size"],
            total_pages=result["total_pages"],
        ).model_dump(),
    )


@router.get("/{archive_id}")
def get_archive(
    archive_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(require_supervisor),
):
    """Get a specific archived record by ID"""
    service = ArchiveService(db, request)
    archive = service.get_by_id_or_404(archive_id)
    return APIResponse(
        success=True,
        message="Archived record retrieved successfully",
        data=ArchiveDataResponse.model_validate(archive).model_dump(),
    )

