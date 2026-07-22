from fastapi import APIRouter, Depends, Query, Request, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.archive_data import ArchiveDataResponse
from app.schemas.common import APIResponse
from app.services.archive_service import ArchiveService
from app.auth.permissions import require_admin, require_supervisor

router = APIRouter(
    prefix="/archive",
    tags=["Archive"],
)


@router.post(
    "/from-main/{main_id}",
    response_model=APIResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Archive a MainData record",
    description="Archives a MainData record. Requires admin role.",
)
def archive_from_main(
    main_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    """Archive a MainData record (Admin only)"""
    service = ArchiveService(db, request)
    archive = service.archive_from_main(main_id, actor_username=current_user.username)
    return APIResponse(
        success=True,
        message="Record archived successfully",
        data=ArchiveDataResponse.model_validate(archive).model_dump(),
    )


@router.get(
    "",
    response_model=APIResponse,
    summary="Get all archived records",
    description="Retrieve all archived records with pagination.",
)
def get_all_archived(
    request: Request,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user=Depends(require_supervisor),
):
    """Get all archived records"""
    service = ArchiveService(db, request)
    records = service.get_all_archived(skip=skip, limit=limit)
    return APIResponse(
        success=True,
        message="Archived records retrieved successfully",
        data=[ArchiveDataResponse.model_validate(r).model_dump() for r in records],
    )


@router.get(
    "/{archive_id}",
    response_model=APIResponse,
    summary="Get an archived record by ID",
    description="Retrieve a specific archived record by its ID.",
)
def get_archived(
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
