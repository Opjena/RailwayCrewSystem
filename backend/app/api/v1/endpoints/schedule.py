from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import date

from app.db.database import get_db
from app.schemas.shift import ShiftCreate, ShiftUpdate, ShiftResponse, ShiftListResponse
from app.schemas.assignment import AssignmentCreate, AssignmentUpdate, AssignmentResponse
from app.schemas.availability import AvailabilityCreate, AvailabilityUpdate, AvailabilityResponse
from app.services.shift_service import ShiftService
from app.services.assignment_service import AssignmentService
from app.services.availability_service import AvailabilityService
from app.auth.permissions import require_admin, require_controller, require_supervisor, require_authenticated

router = APIRouter(
    prefix="/schedule",
    tags=["Schedule & Assignments"],
)

# ==================== SHIFTS ====================


@router.post("/shifts", response_model=ShiftResponse)
def create_shift(
    data: ShiftCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_controller),
):
    """Create a new shift (Controller or Admin)"""
    return ShiftService.create_shift(db, data)


@router.get("/shifts", response_model=list[ShiftListResponse])
def get_all_shifts(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated),
):
    """Get all shifts"""
    return ShiftService.get_all_shifts(db, skip, limit)


@router.get("/shifts/date/{shift_date}", response_model=list[ShiftListResponse])
def get_shifts_by_date(
    shift_date: date,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated),
):
    """Get shifts for a specific date"""
    return ShiftService.get_shifts_by_date(db, shift_date, skip, limit)


@router.get("/shifts/range", response_model=list[ShiftListResponse])
def get_shifts_by_date_range(
    start_date: date,
    end_date: date,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated),
):
    """Get shifts within a date range"""
    return ShiftService.get_shifts_by_date_range(db, start_date, end_date)


@router.get("/shifts/{shift_id}", response_model=ShiftResponse)
def get_shift(
    shift_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated),
):
    """Get a specific shift"""
    return ShiftService.get_shift(db, shift_id)


@router.put("/shifts/{shift_id}", response_model=ShiftResponse)
def update_shift(
    shift_id: int,
    data: ShiftUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_controller),
):
    """Update a shift (Controller or Admin)"""
    return ShiftService.update_shift(db, shift_id, data)


@router.delete("/shifts/{shift_id}")
def delete_shift(
    shift_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_controller),
):
    """Delete a shift (Controller or Admin)"""
    return ShiftService.delete_shift(db, shift_id)


# ==================== ASSIGNMENTS ====================


@router.post("/assignments", response_model=AssignmentResponse)
def create_assignment(
    data: AssignmentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_controller),
):
    """Assign crew to a shift (Controller or Admin)"""
    return AssignmentService.create_assignment(db, data)


@router.get("/assignments", response_model=list[AssignmentResponse])
def get_all_assignments(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated),
):
    """Get all assignments"""
    return AssignmentService.get_all_assignments(db, skip, limit)


@router.get("/assignments/shift/{shift_id}", response_model=list[AssignmentResponse])
def get_assignments_by_shift(
    shift_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated),
):
    """Get all assignments for a specific shift"""
    return AssignmentService.get_assignments_by_shift(db, shift_id)


@router.get("/assignments/crew/{crew_id}", response_model=list[AssignmentResponse])
def get_assignments_by_crew(
    crew_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated),
):
    """Get all assignments for a specific crew member"""
    return AssignmentService.get_assignments_by_crew(db, crew_id, skip, limit)


@router.get("/assignments/{assignment_id}", response_model=AssignmentResponse)
def get_assignment(
    assignment_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated),
):
    """Get a specific assignment"""
    return AssignmentService.get_assignment(db, assignment_id)


@router.put("/assignments/{assignment_id}", response_model=AssignmentResponse)
def update_assignment(
    assignment_id: int,
    data: AssignmentUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_controller),
):
    """Update an assignment (Controller or Admin)"""
    return AssignmentService.update_assignment(db, assignment_id, data)


@router.delete("/assignments/{assignment_id}")
def delete_assignment(
    assignment_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_controller),
):
    """Delete an assignment (Controller or Admin)"""
    return AssignmentService.delete_assignment(db, assignment_id)


# ==================== AVAILABILITY ====================


@router.post("/availability", response_model=AvailabilityResponse)
def create_availability(
    data: AvailabilityCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_supervisor),
):
    """Set crew availability (Supervisor or Admin)"""
    return AvailabilityService.create_availability(db, data)


@router.get("/availability", response_model=list[AvailabilityResponse])
def get_all_availabilities(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated),
):
    """Get all availabilities"""
    return AvailabilityService.get_all_availabilities(db, skip, limit)


@router.get("/availability/crew/{crew_id}", response_model=list[AvailabilityResponse])
def get_crew_availability(
    crew_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated),
):
    """Get availability for a specific crew member"""
    return AvailabilityService.get_crew_availability(db, crew_id, skip, limit)


@router.get("/availability/date/{availability_date}", response_model=list[AvailabilityResponse])
def get_availabilities_by_date(
    availability_date: date,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated),
):
    """Get all availability records for a specific date"""
    return AvailabilityService.get_availabilities_by_date(
        db, availability_date, skip, limit
    )


@router.get("/availability/{availability_id}", response_model=AvailabilityResponse)
def get_availability(
    availability_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated),
):
    """Get a specific availability record"""
    return AvailabilityService.get_availability(db, availability_id)


@router.put("/availability/{availability_id}", response_model=AvailabilityResponse)
def update_availability(
    availability_id: int,
    data: AvailabilityUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_supervisor),
):
    """Update an availability record (Supervisor or Admin)"""
    return AvailabilityService.update_availability(db, availability_id, data)


@router.delete("/availability/{availability_id}")
def delete_availability(
    availability_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_supervisor),
):
    """Delete an availability record (Supervisor or Admin)"""
    return AvailabilityService.delete_availability(db, availability_id)
