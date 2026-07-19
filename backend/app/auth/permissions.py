from fastapi import Depends, HTTPException, status

from app.auth.dependencies import get_current_user
from app.core.enums import UserRole


def require_roles(*allowed_roles: UserRole):
    """
    Generic role-based authorization dependency.
    Usage:
        Depends(require_roles(UserRole.ADMIN))
        Depends(require_roles(UserRole.ADMIN, UserRole.CONTROLLER))
    """

    def role_checker(user=Depends(get_current_user)):
        if user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action.",
            )

        return user

    return role_checker


# Convenience dependencies


require_admin = require_roles(
    UserRole.ADMIN,
)

require_controller = require_roles(
    UserRole.ADMIN,
    UserRole.CONTROLLER,
)

require_supervisor = require_roles(
    UserRole.ADMIN,
    UserRole.CONTROLLER,
    UserRole.SUPERVISOR,
)

require_lobby_operator = require_roles(
    UserRole.ADMIN,
    UserRole.CONTROLLER,
    UserRole.SUPERVISOR,
    UserRole.LOBBY_OPERATOR,
)

require_authenticated = get_current_user