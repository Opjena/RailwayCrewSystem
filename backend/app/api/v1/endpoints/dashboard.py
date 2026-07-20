from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import date, timedelta
from sqlalchemy import func

from app.db.database import get_db
from app.models.shift import Shift
from app.models.assignment import Assignment
from app.models.crew import Crew
from app.models.availability import Availability
from app.auth.permissions import require_authenticated
from app.core.enums import AssignmentStatus, AvailabilityStatus

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard & Analytics"],
)


@router.get("/stats")
def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated),
):
    """Get overall dashboard statistics"""
    today = date.today()

    total_crew = db.query(func.count(Crew.id)).filter(Crew.is_active == True).scalar()
    total_shifts = db.query(func.count(Shift.id)).filter(Shift.shift_date >= today).scalar()
    total_assignments = db.query(func.count(Assignment.id)).scalar()
    active_assignments = (
        db.query(func.count(Assignment.id))
        .filter(Assignment.status == AssignmentStatus.ASSIGNED)
        .scalar()
    )

    unavailable_crew = (
        db.query(func.count(Availability.id))
        .filter(
            Availability.available_date == today,
            Availability.status != AvailabilityStatus.AVAILABLE,
        )
        .scalar()
    )

    return {
        "total_crew": total_crew,
        "total_shifts": total_shifts,
        "total_assignments": total_assignments,
        "active_assignments": active_assignments,
        "unavailable_crew_today": unavailable_crew,
    }


@router.get("/today-shifts")
def get_today_shifts(
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated),
):
    """Get all shifts for today with assignment count"""
    today = date.today()

    shifts = db.query(Shift).filter(Shift.shift_date == today).all()

    shifts_with_count = []
    for shift in shifts:
        assigned_count = (
            db.query(func.count(Assignment.id))
            .filter(
                Assignment.shift_id == shift.id,
                Assignment.status.in_(
                    [AssignmentStatus.ASSIGNED, AssignmentStatus.CONFIRMED]
                ),
            )
            .scalar()
        )

        shifts_with_count.append(
            {
                "id": shift.id,
                "shift_type": shift.shift_type,
                "start_time": str(shift.start_time),
                "end_time": str(shift.end_time),
                "crew_required": shift.crew_required,
                "crew_assigned": assigned_count,
                "location": shift.location,
            }
        )

    return shifts_with_count


@router.get("/upcoming-shifts")
def get_upcoming_shifts(
    days: int = Query(7, ge=1, le=90),
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated),
):
    """Get upcoming shifts for the next N days"""
    today = date.today()
    end_date = today + timedelta(days=days)

    shifts = (
        db.query(Shift)
        .filter(Shift.shift_date >= today, Shift.shift_date <= end_date)
        .order_by(Shift.shift_date)
        .all()
    )

    shifts_with_count = []
    for shift in shifts:
        assigned_count = (
            db.query(func.count(Assignment.id))
            .filter(
                Assignment.shift_id == shift.id,
                Assignment.status.in_(
                    [AssignmentStatus.ASSIGNED, AssignmentStatus.CONFIRMED]
                ),
            )
            .scalar()
        )

        shifts_with_count.append(
            {
                "id": shift.id,
                "shift_date": str(shift.shift_date),
                "shift_type": shift.shift_type,
                "start_time": str(shift.start_time),
                "end_time": str(shift.end_time),
                "crew_required": shift.crew_required,
                "crew_assigned": assigned_count,
                "coverage_percent": round(
                    (assigned_count / shift.crew_required * 100)
                    if shift.crew_required > 0
                    else 0
                ),
            }
        )

    return shifts_with_count


@router.get("/crew-utilization")
def get_crew_utilization(
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated),
):
    """Get crew utilization for the last N days"""
    today = date.today()
    start_date = today - timedelta(days=days)

    crew_members = db.query(Crew).filter(Crew.is_active == True).all()

    utilization_data = []
    for crew in crew_members:
        assignments = (
            db.query(func.count(Assignment.id))
            .join(Shift)
            .filter(
                Assignment.crew_id == crew.id,
                Shift.shift_date >= start_date,
                Shift.shift_date <= today,
                Assignment.status != AssignmentStatus.CANCELLED,
            )
            .scalar()
        )

        utilization_data.append(
            {
                "crew_id": crew.id,
                "crew_name": crew.full_name,
                "department": crew.department,
                "assignments_count": assignments,
            }
        )

    return utilization_data


@router.get("/shift-coverage")
def get_shift_coverage(
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated),
):
    """Get shift coverage statistics by shift type"""
    today = date.today()

    shifts = db.query(Shift).filter(Shift.shift_date >= today).all()

    coverage_by_type = {}
    for shift in shifts:
        shift_type = shift.shift_type.value

        if shift_type not in coverage_by_type:
            coverage_by_type[shift_type] = {"total_shifts": 0, "total_crew_needed": 0, "total_crew_assigned": 0}

        coverage_by_type[shift_type]["total_shifts"] += 1
        coverage_by_type[shift_type]["total_crew_needed"] += shift.crew_required

        assigned = (
            db.query(func.count(Assignment.id))
            .filter(
                Assignment.shift_id == shift.id,
                Assignment.status.in_(
                    [AssignmentStatus.ASSIGNED, AssignmentStatus.CONFIRMED]
                ),
            )
            .scalar()
        )
        coverage_by_type[shift_type]["total_crew_assigned"] += assigned

    result = []
    for shift_type, stats in coverage_by_type.items():
        result.append(
            {
                "shift_type": shift_type,
                "total_shifts": stats["total_shifts"],
                "total_crew_needed": stats["total_crew_needed"],
                "total_crew_assigned": stats["total_crew_assigned"],
                "coverage_percent": round(
                    (stats["total_crew_assigned"] / stats["total_crew_needed"] * 100)
                    if stats["total_crew_needed"] > 0
                    else 0
                ),
            }
        )

    return result
