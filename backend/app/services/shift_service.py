from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import date

from app.models.shift import Shift
from app.repositories.shift_repository import ShiftRepository
from app.schemas.shift import ShiftCreate, ShiftUpdate


class ShiftService:

    @staticmethod
    def create_shift(db: Session, data: ShiftCreate):
        # Validate times
        if data.start_time >= data.end_time:
            raise HTTPException(
                status_code=400,
                detail="Start time must be before end time",
            )

        # Validate date is not in the past
        if data.shift_date < date.today():
            raise HTTPException(
                status_code=400,
                detail="Shift date cannot be in the past",
            )

        shift = Shift(
            shift_date=data.shift_date,
            shift_type=data.shift_type,
            start_time=data.start_time,
            end_time=data.end_time,
            crew_required=data.crew_required,
            location=data.location,
            notes=data.notes,
        )

        return ShiftRepository.create(db, shift)

    @staticmethod
    def get_all_shifts(db: Session, skip: int = 0, limit: int = 100):
        return ShiftRepository.get_all(db, skip, limit)

    @staticmethod
    def get_shift(db: Session, shift_id: int):
        shift = ShiftRepository.get_by_id(db, shift_id)

        if not shift:
            raise HTTPException(
                status_code=404,
                detail="Shift not found",
            )

        return shift

    @staticmethod
    def update_shift(db: Session, shift_id: int, data: ShiftUpdate):
        shift = ShiftService.get_shift(db, shift_id)

        # Validate times if both provided
        if data.start_time and data.end_time:
            if data.start_time >= data.end_time:
                raise HTTPException(
                    status_code=400,
                    detail="Start time must be before end time",
                )
        elif data.start_time and shift.end_time:
            if data.start_time >= shift.end_time:
                raise HTTPException(
                    status_code=400,
                    detail="Start time must be before end time",
                )
        elif data.end_time and shift.start_time:
            if shift.start_time >= data.end_time:
                raise HTTPException(
                    status_code=400,
                    detail="End time must be after start time",
                )

        update_data = data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(shift, key, value)

        ShiftRepository.update(db)

        return shift

    @staticmethod
    def delete_shift(db: Session, shift_id: int):
        shift = ShiftService.get_shift(db, shift_id)
        ShiftRepository.delete(db, shift)

        return {"message": "Shift deleted successfully"}

    @staticmethod
    def get_shifts_by_date(db: Session, shift_date: date, skip: int = 0, limit: int = 100):
        return ShiftRepository.get_by_date(db, shift_date, skip, limit)

    @staticmethod
    def get_shifts_by_date_range(db: Session, start_date: date, end_date: date):
        if start_date > end_date:
            raise HTTPException(
                status_code=400,
                detail="Start date must be before end date",
            )

        return ShiftRepository.get_by_date_range(db, start_date, end_date)
