from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.schemas.auth import LoginRequest, Token

from app.auth.auth_service import authenticate_user

from app.auth.jwt import create_access_token

router = APIRouter()


@router.post("/login", response_model=Token)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db),
):

    user = authenticate_user(
        db,
        request.username,
        request.password,
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
        )

    token = create_access_token(
        {
            "sub": user.username,
            "role": user.role,
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer",
    }