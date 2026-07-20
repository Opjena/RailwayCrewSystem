from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import date, timedelta
from sqlalchemy import func

from app.db.database import get_db
from app.models.shift import Shift
from app.models.assignment import Assignment
from app.models.crew import Crew
from app.models.availability import Availability
from app.auth.permissions import require_controller
from app.core.enums import AssignmentStatus, AvailabilityStatus, Department

router = APIRouter(
    prefix="/reports",
    tags=["Reports"],
)


@router.get("/crew-assignments")
def get_crew_assignments_report(
    start_date: date,
    end_date: date,
    department: str | None = None,
    db: Session = Depends(get_db),
    current_user=Depends(require_controller),
):
    """Generate crew assignments report for a date range"""
    query = (
        db.query(
            Crew.crew_id,
            Crew.full_name,
            Crew.department,
            func.count(Assignment.id).label("total_assignments"),
        )
        .outerjoin(Assignment)
        .join(Shift, Assignment.shift_id == Shift.id, isouter=True)
        .filter(Shift.shift_date >= start_date, Shift.shift_date <= end_date)
        .group_by(Crew.id)
    )

    if department:
        try:
            dept_enum = Department[department.upper()]
            query = query.filter(Crew.department == dept_enum)
        except KeyError:
            pass

    results = query.all()

    return [
        {
            "crew_id": r[0],
            "full_name": r[1],
            "department": r[2],
            "total_assignments": r[3] or 0,
        }
        for r in results
    ]


@router.get("/shift-utilization")
def get_shift_utilization_report(
    start_date: date,
    end_date: date,
    db: Session = Depends(get_db),
    current_user=Depends(require_controller),
):
    """Generate shift utilization report"""
    shifts = (
        db.query(Shift)
        .filter(Shift.shift_date >= start_date, Shift.shift_date <= end_date)
        .order_by(Shift.shift_date)
        .all()
    )

    report = []
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

        report.append(
            {
                "shift_id": shift.id,
                "shift_date": str(shift.shift_date),
                "shift_type": shift.shift_type,
                "crew_required": shift.crew_required,
                "crew_assigned": assigned_count,
                "shortfall": max(0, shift.crew_required - assigned_count),
                "coverage_percent": round(
                    (assigned_count / shift.crew_required * 100)
                    if shift.crew_required > 0
                    else 0
                ),
            }
        )

    return report


@router.get("/department-summary")
def get_department_summary_report(
    start_date: date,
    end_date: date,
    db: Session = Depends(get_db),
    current_user=Depends(require_controller),
):
    """Generate department-wise summary report"""
    summary = []
    for dept in Department:
        crew_count = db.query(func.count(Crew.id)).filter(
            Crew.department == dept, Crew.is_active == True
        ).scalar()

        total_assignments = (
            db.query(func.count(Assignment.id))
            .join(Crew)
            .join(Shift, Assignment.shift_id == Shift.id)
            .filter(
                Crew.department == dept,
                Shift.shift_date >= start_date,
                Shift.shift_date <= end_date,
            )
            .scalar()
        )

        completed_assignments = (
            db.query(func.count(Assignment.id))
            .join(Crew)
            .join(Shift, Assignment.shift_id == Shift.id)
            .filter(
                Crew.department == dept,
                Shift.shift_date >= start_date,
                Shift.shift_date <= end_date,
                Assignment.status == AssignmentStatus.COMPLETED,
            )
            .scalar()
        )

        summary.append(
            {
                "department": dept.value,
                "active_crew": crew_count,
                "total_assignments": total_assignments,
                "completed_assignments": completed_assignments,
                "completion_rate": round(
                    (completed_assignments / total_assignments * 100)
                    if total_assignments > 0
                    else 0
                ),
            }
        )

    return summary


@router.get("/availability-report")
def get_availability_report(
    start_date: date,
    end_date: date,
    db: Session = Depends(get_db),
    current_user=Depends(require_controller),
):
    """Generate availability report for a date range"""
    availabilities = (
        db.query(Availability)
        .filter(
            Availability.available_date >= start_date,
            Availability.available_date <= end_date,
        )
        .order_by(Availability.available_date)
        .all()
    )

    status_breakdown = {}
    for avail in availabilities:
        status = avail.status.value
        if status not in status_breakdown:
            status_breakdown[status] = 0
        status_breakdown[status] += 1

    return {
        "period": {
            "start_date": str(start_date),
            "end_date": str(end_date),
        },
        "total_records": len(availabilities),
        "status_breakdown": status_breakdown,
    }
