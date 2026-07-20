from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.auth.permissions import require_admin

router = APIRouter(
    prefix="/settings",
    tags=["Settings"],
)


@router.get("/system-config")
def get_system_config(
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    """Get system configuration (Admin only)"""
    return {
        "system_name": "Railway Crew Management System",
        "version": "1.0.0",
        "features": {
            "crew_management": True,
            "shift_scheduling": True,
            "availability_tracking": True,
            "reporting": True,
            "dashboard": True,
        },
        "max_crew_per_shift": 50,
        "default_shift_duration_hours": 8,
        "system_status": "operational",
    }


@router.get("/departments")
def get_departments(
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    """Get list of available departments"""
    from app.core.enums import Department

    return [
        {"name": dept.value, "key": dept.name}
        for dept in Department
    ]


@router.get("/shift-types")
def get_shift_types(
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    """Get list of available shift types"""
    from app.core.enums import ShiftType

    return [
        {"name": shift.value, "key": shift.name}
        for shift in ShiftType
    ]


@router.get("/user-roles")
def get_user_roles(
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    """Get list of available user roles"""
    from app.core.enums import UserRole

    return [
        {"name": role.value, "key": role.name}
        for role in UserRole
    ]
