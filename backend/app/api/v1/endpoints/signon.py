from fastapi import APIRouter, Depends, Query, Request, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.signon_data import SignOnDataCreate, SignOnDataUpdate, SignOnDataResponse
from app.schemas.common import APIResponse
from app.services.signon_service import SignOnService
from app.auth.permissions import require_admin, require_supervisor

router = APIRouter(
    prefix="/signon",
    tags=["SignOn"],
)


@router.post(
    "",
    response_model=APIResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new SignOn record",
    description="Creates a SignOn record for a crew member. Requires admin role.",
)
def create_signon(
    data: SignOnDataCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    """Create a new SignOn record (Admin only)"""
    service = SignOnService(db, request)
    signon = service.create_signon(data, actor_username=current_user.username)
    return APIResponse(
        success=True,
        message="SignOn record created successfully",
        data=SignOnDataResponse.model_validate(signon).model_dump(),
    )


@router.get(
    "",
    response_model=APIResponse,
    summary="Get all SignOn records",
    description="Retrieve all SignOn records with pagination.",
)
def get_all_signon(
    request: Request,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user=Depends(require_supervisor),
):
    """Get all SignOn records"""
    service = SignOnService(db, request)
    signons = service.get_all_signon(skip=skip, limit=limit)
    return APIResponse(
        success=True,
        message="SignOn records retrieved successfully",
        data=[SignOnDataResponse.model_validate(s).model_dump() for s in signons],
    )


@router.get(
    "/{signon_id}",
    response_model=APIResponse,
    summary="Get a SignOn record by ID",
    description="Retrieve a specific SignOn record by its ID.",
)
def get_signon(
    signon_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(require_supervisor),
):
    """Get a specific SignOn record by ID"""
    service = SignOnService(db, request)
    signon = service.get_by_id_or_404(signon_id)
    return APIResponse(
        success=True,
        message="SignOn record retrieved successfully",
        data=SignOnDataResponse.model_validate(signon).model_dump(),
    )


@router.put(
    "/{signon_id}",
    response_model=APIResponse,
    summary="Update a SignOn record",
    description="Update an existing SignOn record. Requires admin role.",
)
def update_signon(
    signon_id: int,
    data: SignOnDataUpdate,
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    """Update a SignOn record (Admin only)"""
    service = SignOnService(db, request)
    signon = service.update_signon(signon_id, data, actor_username=current_user.username)
    return APIResponse(
        success=True,
        message="SignOn record updated successfully",
        data=SignOnDataResponse.model_validate(signon).model_dump(),
    )


@router.delete(
    "/{signon_id}",
    response_model=APIResponse,
    summary="Deactivate a SignOn record",
    description="Soft-delete (deactivate) a SignOn record. Requires admin role.",
)
def delete_signon(
    signon_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    """Deactivate (soft delete) a SignOn record (Admin only)"""
    service = SignOnService(db, request)
    result = service.delete_signon(signon_id, actor_username=current_user.username)
    return APIResponse(
        success=True,
        message=result["message"],
    )
