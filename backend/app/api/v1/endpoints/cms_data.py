from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.cms_data import CMSDataCreate, CMSDataUpdate, CMSDataResponse
from app.schemas.common import APIResponse, PaginatedResponse
from app.services.cms_service import CMSService
from app.auth.permissions import require_admin, require_supervisor

router = APIRouter(
    prefix="/cms",
    tags=["CMS Data"],
)


@router.post("")
def create_cms(
    data: CMSDataCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    """Create a new CMS record (Admin only)"""
    service = CMSService(db, request)
    cms = service.create_cms(data, actor_username=current_user.username)
    return APIResponse(
        success=True,
        message="CMS record created successfully",
        data=CMSDataResponse.model_validate(cms).model_dump(),
    )


@router.get("")
def get_all_cms(
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
    """Get all CMS records with pagination, filtering, and search"""
    service = CMSService(db, request)
    result = service.get_all_cms(
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
        message="CMS records retrieved successfully",
        data=PaginatedResponse(
            items=[
                CMSDataResponse.model_validate(c).model_dump() for c in result["items"]
            ],
            total=result["total"],
            page=result["page"],
            page_size=result["page_size"],
            total_pages=result["total_pages"],
        ).model_dump(),
    )


@router.get("/{cms_id}")
def get_cms(
    cms_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(require_supervisor),
):
    """Get a specific CMS record by ID"""
    service = CMSService(db, request)
    cms = service.get_by_id_or_404(cms_id)
    return APIResponse(
        success=True,
        message="CMS record retrieved successfully",
        data=CMSDataResponse.model_validate(cms).model_dump(),
    )


@router.put("/{cms_id}")
def update_cms(
    cms_id: int,
    data: CMSDataUpdate,
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    """Update a CMS record (Admin only)"""
    service = CMSService(db, request)
    cms = service.update_cms(cms_id, data, actor_username=current_user.username)
    return APIResponse(
        success=True,
        message="CMS record updated successfully",
        data=CMSDataResponse.model_validate(cms).model_dump(),
    )


@router.delete("/{cms_id}")
def delete_cms(
    cms_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    """Deactivate (soft delete) a CMS record (Admin only)"""
    service = CMSService(db, request)
    result = service.delete_cms(cms_id, actor_username=current_user.username)
    return APIResponse(
        success=True,
        message=result["message"],
    )

