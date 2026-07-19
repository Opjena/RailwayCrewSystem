from sqlalchemy.orm import Session

from app.auth.hashing import verify_password

from app.repositories.user_repository import UserRepository


def authenticate_user(
    db: Session,
    username: str,
    password: str,
):

    user = UserRepository.get_by_username(
        db,
        username,
    )

    if not user:
        return None

    if not verify_password(
        password,
        user.password_hash,
    ):
        return None

    return user