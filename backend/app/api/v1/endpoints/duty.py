from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.auth.permissions import require_authenticated, require_controller
from app.db.database import get_db
from app.models.duty import Duty
from app.schemas.duty import DutyCreate, DutyResponse, DutyUpdate
from app.services.audit_log_service import AuditLogService

router = APIRouter(prefix="/duty", tags=["Duty"])


@router.post("", response_model=DutyResponse)
def create_duty(
    data: DutyCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_controller),
):
    existing = db.query(Duty).filter(Duty.duty_code == data.duty_code).first()
    if existing:
        raise HTTPException(status_code=400, detail="Duty code already exists")

    duty = Duty(
        duty_code=data.duty_code,
        description=data.description,
        is_active=data.is_active,
    )
    db.add(duty)
    db.commit()
    db.refresh(duty)
    AuditLogService.log_action(
        db,
        actor_username=current_user.username,
        action="create",
        entity="duty",
        entity_id=str(duty.id),
    )
    return duty


@router.get("", response_model=list[DutyResponse])
def list_duties(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated),
):
    return db.query(Duty).offset(skip).limit(limit).all()


@router.get("/{duty_id}", response_model=DutyResponse)
def get_duty(
    duty_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated),
):
    duty = db.query(Duty).filter(Duty.id == duty_id).first()
    if not duty:
        raise HTTPException(status_code=404, detail="Duty not found")
    return duty


@router.put("/{duty_id}", response_model=DutyResponse)
def update_duty(
    duty_id: int,
    data: DutyUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_controller),
):
    duty = db.query(Duty).filter(Duty.id == duty_id).first()
    if not duty:
        raise HTTPException(status_code=404, detail="Duty not found")

    if data.duty_code and data.duty_code != duty.duty_code:
        existing = db.query(Duty).filter(Duty.duty_code == data.duty_code).first()
        if existing:
            raise HTTPException(status_code=400, detail="Duty code already exists")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(duty, key, value)
    db.commit()
    db.refresh(duty)
    AuditLogService.log_action(
        db,
        actor_username=current_user.username,
        action="update",
        entity="duty",
        entity_id=str(duty.id),
    )
    return duty


@router.delete("/{duty_id}")
def delete_duty(
    duty_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_controller),
):
    duty = db.query(Duty).filter(Duty.id == duty_id).first()
    if not duty:
        raise HTTPException(status_code=404, detail="Duty not found")

    db.delete(duty)
    db.commit()
    AuditLogService.log_action(
        db,
        actor_username=current_user.username,
        action="delete",
        entity="duty",
        entity_id=str(duty_id),
    )
    return {"message": "Duty deleted successfully"}
