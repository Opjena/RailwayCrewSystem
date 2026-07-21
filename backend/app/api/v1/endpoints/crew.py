from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.crew import CrewCreate, CrewUpdate, CrewResponse, CrewListResponse
from app.services.crew_service import CrewService
from app.auth.permissions import require_admin, require_supervisor

router = APIRouter(
    prefix="/crew",
    tags=["Crew Management"],
)


@router.post("", response_model=CrewResponse)
def create_crew(
    data: CrewCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    """Create a new crew member (Admin only)"""
    return CrewService.create_crew(db, data)


@router.get("", response_model=CrewListResponse)
def get_all_crew(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user=Depends(require_supervisor),
):
    """Get all crew members (Admin, Controller, Supervisor)"""
    return CrewService.get_all_crew(db, skip, limit)


@router.get("/{crew_id}", response_model=CrewResponse)
def get_crew(
    crew_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(require_supervisor),
):
    """Get a specific crew member by crew_id (Admin, Controller, Supervisor)"""
    return CrewService.get_crew_by_crew_id(db, crew_id)


@router.put("/{crew_id}", response_model=CrewResponse)
def update_crew(
    crew_id: str,
    data: CrewUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    """Update a crew member (Admin only)"""
    return CrewService.update_crew(db, crew_id, data)


@router.delete("/{crew_id}")
def delete_crew(
    crew_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    """Delete a crew member (Admin only)"""
    return CrewService.delete_crew(db, crew_id)

