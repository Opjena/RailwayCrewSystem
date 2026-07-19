from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.auth.hashing import hash_password
from app.core.enums import UserRole
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate


class UserService:

    @staticmethod
    def create_user(db: Session, data: UserCreate):

        if UserRepository.get_by_username(db, data.username):
            raise HTTPException(
                status_code=400,
                detail="Username already exists",
            )

        if UserRepository.get_by_email(db, data.email):
            raise HTTPException(
                status_code=400,
                detail="Email already exists",
            )

        user = User(
            username=data.username,
            full_name=data.full_name,
            email=data.email,
            password_hash=hash_password(data.password),
            role=data.role,
            is_active=True,
        )

        return UserRepository.create(db, user)

    @staticmethod
    def get_all_users(db: Session):
        return UserRepository.get_all(db)

    @staticmethod
    def get_user(db: Session, user_id: int):

        user = UserRepository.get_by_id(db, user_id)

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found",
            )

        return user

    @staticmethod
    def update_user(
        db: Session,
        user_id: int,
        data: UserUpdate,
    ):

        user = UserService.get_user(db, user_id)

        update_data = data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(user, key, value)

        UserRepository.update(db)

        return user

    @staticmethod
    def delete_user(
        db: Session,
        user_id: int,
    ):

        user = UserService.get_user(db, user_id)

        UserRepository.delete(db, user)

        return {
            "message": "User deleted successfully"
        }