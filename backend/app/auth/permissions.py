from fastapi import Depends, HTTPException

from app.auth.dependencies import get_current_user


def require_admin(user=Depends(get_current_user)):

    if user.role != "Admin":

        raise HTTPException(
            status_code=403,
            detail="Admin access required",
        )

    return user


def require_controller(user=Depends(get_current_user)):

    if user.role not in ["Admin", "Controller"]:

        raise HTTPException(
            status_code=403,
            detail="Controller access required",
        )

    return user