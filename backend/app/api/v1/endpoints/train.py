from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.auth.permissions import require_authenticated, require_controller
from app.db.database import get_db
from app.models.train import Train
from app.schemas.train import TrainCreate, TrainResponse, TrainUpdate
from app.services.audit_log_service import AuditLogService

router = APIRouter(prefix="/train", tags=["Train"])


@router.post("", response_model=TrainResponse)
def create_train(
    data: TrainCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_controller),
):
    existing = db.query(Train).filter(Train.train_number == data.train_number).first()
    if existing:
        raise HTTPException(status_code=400, detail="Train number already exists")

    train = Train(train_number=data.train_number, is_active=data.is_active)
    db.add(train)
    db.commit()
    db.refresh(train)
    AuditLogService.log_action(
        db,
        actor_username=current_user.username,
        action="create",
        entity="train",
        entity_id=str(train.id),
    )
    return train


@router.get("", response_model=list[TrainResponse])
def list_trains(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated),
):
    return db.query(Train).offset(skip).limit(limit).all()


@router.get("/{train_id}", response_model=TrainResponse)
def get_train(
    train_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated),
):
    train = db.query(Train).filter(Train.id == train_id).first()
    if not train:
        raise HTTPException(status_code=404, detail="Train not found")
    return train


@router.put("/{train_id}", response_model=TrainResponse)
def update_train(
    train_id: int,
    data: TrainUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_controller),
):
    train = db.query(Train).filter(Train.id == train_id).first()
    if not train:
        raise HTTPException(status_code=404, detail="Train not found")

    if data.train_number and data.train_number != train.train_number:
        existing = db.query(Train).filter(Train.train_number == data.train_number).first()
        if existing:
            raise HTTPException(status_code=400, detail="Train number already exists")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(train, key, value)
    db.commit()
    db.refresh(train)
    AuditLogService.log_action(
        db,
        actor_username=current_user.username,
        action="update",
        entity="train",
        entity_id=str(train.id),
    )
    return train


@router.delete("/{train_id}")
def delete_train(
    train_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_controller),
):
    train = db.query(Train).filter(Train.id == train_id).first()
    if not train:
        raise HTTPException(status_code=404, detail="Train not found")

    db.delete(train)
    db.commit()
    AuditLogService.log_action(
        db,
        actor_username=current_user.username,
        action="delete",
        entity="train",
        entity_id=str(train_id),
    )
    return {"message": "Train deleted successfully"}
