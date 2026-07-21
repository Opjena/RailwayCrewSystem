from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.auth.permissions import require_authenticated, require_controller
from app.db.database import get_db
from app.models.lobby import Lobby
from app.schemas.lobby import LobbyCreate, LobbyResponse, LobbyUpdate
from app.services.audit_log_service import AuditLogService

router = APIRouter(prefix="/lobby", tags=["Lobby"])


@router.post("", response_model=LobbyResponse)
def create_lobby(
    data: LobbyCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_controller),
):
    existing = db.query(Lobby).filter(Lobby.name == data.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Lobby name already exists")

    lobby = Lobby(name=data.name, is_active=data.is_active)
    db.add(lobby)
    db.commit()
    db.refresh(lobby)
    AuditLogService.log_action(
        db,
        actor_username=current_user.username,
        action="create",
        entity="lobby",
        entity_id=str(lobby.id),
    )
    return lobby


@router.get("", response_model=list[LobbyResponse])
def list_lobbies(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated),
):
    return db.query(Lobby).offset(skip).limit(limit).all()


@router.get("/{lobby_id}", response_model=LobbyResponse)
def get_lobby(
    lobby_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated),
):
    lobby = db.query(Lobby).filter(Lobby.id == lobby_id).first()
    if not lobby:
        raise HTTPException(status_code=404, detail="Lobby not found")
    return lobby


@router.put("/{lobby_id}", response_model=LobbyResponse)
def update_lobby(
    lobby_id: int,
    data: LobbyUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_controller),
):
    lobby = db.query(Lobby).filter(Lobby.id == lobby_id).first()
    if not lobby:
        raise HTTPException(status_code=404, detail="Lobby not found")

    if data.name and data.name != lobby.name:
        existing = db.query(Lobby).filter(Lobby.name == data.name).first()
        if existing:
            raise HTTPException(status_code=400, detail="Lobby name already exists")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(lobby, key, value)
    db.commit()
    db.refresh(lobby)
    AuditLogService.log_action(
        db,
        actor_username=current_user.username,
        action="update",
        entity="lobby",
        entity_id=str(lobby.id),
    )
    return lobby


@router.delete("/{lobby_id}")
def delete_lobby(
    lobby_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_controller),
):
    lobby = db.query(Lobby).filter(Lobby.id == lobby_id).first()
    if not lobby:
        raise HTTPException(status_code=404, detail="Lobby not found")

    db.delete(lobby)
    db.commit()
    AuditLogService.log_action(
        db,
        actor_username=current_user.username,
        action="delete",
        entity="lobby",
        entity_id=str(lobby_id),
    )
    return {"message": "Lobby deleted successfully"}
