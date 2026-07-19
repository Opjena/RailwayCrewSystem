from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.schemas.user import (
    UserCreate,
    UserUpdate,
    UserResponse,
)

from app.services.user_service import UserService

from app.auth.permissions import (
    require_admin,
    require_authenticated,
)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post(
    "",
    response_model=UserResponse,
)
def create_user(
    data: UserCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    return UserService.create_user(
        db,
        data,
    )


@router.get(
    "",
    response_model=list[UserResponse],
)
def get_users(
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated),
):
    return UserService.get_all_users(db)


@router.get(
    "/me",
    response_model=UserResponse,
)
def get_me(
    current_user=Depends(require_authenticated),
):
    return current_user


@router.get(
    "/{user_id}",
    response_model=UserResponse,
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated),
):
    return UserService.get_user(
        db,
        user_id,
    )


@router.put(
    "/{user_id}",
    response_model=UserResponse,
)
def update_user(
    user_id: int,
    data: UserUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    return UserService.update_user(
        db,
        user_id,
        data,
    )


@router.delete(
    "/{user_id}",
)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    return UserService.delete_user(
        db,
        user_id,
    )