from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.crew import CrewCreate, CrewUpdate, CrewResponse
from app.schemas.common import APIResponse, PaginatedResponse
from app.services.crew_service import CrewService
from app.auth.permissions import require_admin, require_authenticated

router = APIRouter(
    prefix="/crew",
    tags=["Crew Management"],
)


@router.post("")
def create_crew(
    data: CrewCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    """Create a new crew member (Admin only)"""
    service = CrewService(db, request)
    crew = service.create_crew(data, actor_username=current_user.username)
    return APIResponse(
        success=True,
        message="Crew created successfully",
        data=CrewResponse.model_validate(crew).model_dump(),
    )


@router.get("")
def get_all_crew(
    request: Request,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=1000),
    department: str | None = Query(None, description="Filter by department"),
    is_active: bool | None = Query(None, description="Filter by active status"),
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated),
):
    """Get all crew members (Admin, Controller, Supervisor)"""
    service = CrewService(db, request)
    result = service.get_all_crew(skip, limit, department, is_active)
    return APIResponse(
        success=True,
        message="Crew retrieved successfully",
        data=PaginatedResponse(
            items=[
                CrewResponse.model_validate(c).model_dump() for c in result["items"]
            ],
            total=result["total"],
            page=result["page"],
            page_size=result["page_size"],
            total_pages=result["total_pages"],
        ).model_dump(),
    )


@router.get("/{crew_id}")
def get_crew(
    crew_id: str,
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated),
):
    """Get a specific crew member by crew_id (All authenticated users)"""
    service = CrewService(db, request)
    crew = service.get_crew_by_crew_id(crew_id)
    return APIResponse(
        success=True,
        message="Crew retrieved successfully",
        data=CrewResponse.model_validate(crew).model_dump(),
    )


@router.put("/{crew_id}")
def update_crew(
    crew_id: str,
    data: CrewUpdate,
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    """Update a crew member (Admin only)"""
    service = CrewService(db, request)
    crew = service.update_crew(crew_id, data, actor_username=current_user.username)
    return APIResponse(
        success=True,
        message="Crew updated successfully",
        data=CrewResponse.model_validate(crew).model_dump(),
    )


@router.delete("/{crew_id}")
def deactivate_crew(
    crew_id: str,
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    """Deactivate a crew member (soft delete) (Admin only)"""
    service = CrewService(db, request)
    result = service.delete_crew(crew_id, actor_username=current_user.username)
    return APIResponse(
        success=True,
        message=result["message"],
    )

