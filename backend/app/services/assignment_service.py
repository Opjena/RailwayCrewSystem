from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.assignment import Assignment
from app.repositories.assignment_repository import AssignmentRepository
from app.repositories.shift_repository import ShiftRepository
from app.repositories.crew_repository import CrewRepository
from app.repositories.availability_repository import AvailabilityRepository
from app.schemas.assignment import AssignmentCreate, AssignmentUpdate
from app.core.enums import AvailabilityStatus


class AssignmentService:

    @staticmethod
    def create_assignment(db: Session, data: AssignmentCreate):
        # Verify shift exists
        shift = ShiftRepository.get_by_id(db, data.shift_id)
        if not shift:
            raise HTTPException(
                status_code=404,
                detail="Shift not found",
            )

        # Verify crew exists
        crew = CrewRepository.get_by_id(db, data.crew_id)
        if not crew:
            raise HTTPException(
                status_code=404,
                detail="Crew not found",
            )

        if not crew.is_active:
            raise HTTPException(
                status_code=400,
                detail="Crew is inactive",
            )

        # Check if assignment already exists
        existing = AssignmentRepository.get_by_shift_and_crew(
            db, data.shift_id, data.crew_id
        )
        if existing:
            raise HTTPException(
                status_code=400,
                detail="Assignment already exists for this crew and shift",
            )

        # Check crew availability
        availability = AvailabilityRepository.get_by_crew_and_date(
            db, data.crew_id, shift.shift_date
        )
        if availability and availability.status != AvailabilityStatus.AVAILABLE:
            raise HTTPException(
                status_code=400,
                detail=f"Crew is {availability.status.value} on this date",
            )

        assignment = Assignment(
            shift_id=data.shift_id,
            crew_id=data.crew_id,
            status=data.status,
        )

        return AssignmentRepository.create(db, assignment)

    @staticmethod
    def get_all_assignments(db: Session, skip: int = 0, limit: int = 100):
        return AssignmentRepository.get_all(db, skip, limit)

    @staticmethod
    def get_assignment(db: Session, assignment_id: int):
        assignment = AssignmentRepository.get_by_id(db, assignment_id)

        if not assignment:
            raise HTTPException(
                status_code=404,
                detail="Assignment not found",
            )

        return assignment

    @staticmethod
    def update_assignment(db: Session, assignment_id: int, data: AssignmentUpdate):
        assignment = AssignmentService.get_assignment(db, assignment_id)

        update_data = data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(assignment, key, value)

        AssignmentRepository.update(db)

        return assignment

    @staticmethod
    def delete_assignment(db: Session, assignment_id: int):
        assignment = AssignmentService.get_assignment(db, assignment_id)
        AssignmentRepository.delete(db, assignment)

        return {"message": "Assignment deleted successfully"}

    @staticmethod
    def get_assignments_by_shift(db: Session, shift_id: int):
        shift = ShiftRepository.get_by_id(db, shift_id)
        if not shift:
            raise HTTPException(
                status_code=404,
                detail="Shift not found",
            )

        return AssignmentRepository.get_by_shift(db, shift_id)

    @staticmethod
    def get_assignments_by_crew(db: Session, crew_id: int, skip: int = 0, limit: int = 100):
        crew = CrewRepository.get_by_id(db, crew_id)
        if not crew:
            raise HTTPException(
                status_code=404,
                detail="Crew not found",
            )

        return AssignmentRepository.get_by_crew(db, crew_id, skip, limit)
