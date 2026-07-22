from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.signon_data import SignOnDataCreate, SignOnDataUpdate, SignOnDataResponse
from app.schemas.main_data import MainDataResponse
from app.schemas.common import APIResponse, PaginatedResponse
from app.services.signon_service import SignOnService
from app.auth.permissions import require_admin, require_supervisor

router = APIRouter(
    prefix="/signon",
    tags=["Sign On"],
)


@router.post("")
def create_signon(
    data: SignOnDataCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    """
    Create a new SignOn record.

    Business workflow (single transaction):
      1. Verify Crew exists in master
      2. Verify CMS record exists
      3. Create SignOn
      4. Create MainData snapshot
      5. Audit Log
    """
    service = SignOnService(db, request)
    result = service.create_signon(data, actor_username=current_user.username)
    return APIResponse(
        success=True,
        message="SignOn created successfully",
        data={
            "signon": SignOnDataResponse.model_validate(result["signon"]).model_dump(),
            "main_data": MainDataResponse.model_validate(result["main_data"]).model_dump(),
        },
    )


@router.get("")
def get_all_signon(
    request: Request,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=1000),
    crew_id: str | None = Query(None, description="Filter by crew ID"),
    status: str | None = Query(None, description="Filter by status"),
    is_active: bool | None = Query(None, description="Filter by active status"),
    search: str | None = Query(None, description="Keyword search"),
    sort: str = Query("id", description="Sort column"),
    order: str = Query("asc", description="Sort order (asc/desc)"),
    db: Session = Depends(get_db),
    current_user=Depends(require_supervisor),
):
    """Get all SignOn records with pagination, filtering, and search"""
    service = SignOnService(db, request)
    result = service.get_all_signon(
        skip=skip,
        limit=limit,
        crew_id=crew_id,
        status=status,
        is_active=is_active,
        search=search,
        sort=sort,
        order=order,
    )
    return APIResponse(
        success=True,
        message="SignOn records retrieved successfully",
        data=PaginatedResponse(
            items=[
                SignOnDataResponse.model_validate(s).model_dump()
                for s in result["items"]
            ],
            total=result["total"],
            page=result["page"],
            page_size=result["page_size"],
            total_pages=result["total_pages"],
        ).model_dump(),
    )


@router.get("/{signon_id}")
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


@router.put("/{signon_id}")
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


@router.delete("/{signon_id}")
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

