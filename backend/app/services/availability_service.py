from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import date

from app.models.availability import Availability
from app.repositories.availability_repository import AvailabilityRepository
from app.repositories.crew_repository import CrewRepository
from app.schemas.availability import AvailabilityCreate, AvailabilityUpdate


class AvailabilityService:

    @staticmethod
    def create_availability(db: Session, data: AvailabilityCreate):
        # Verify crew exists
        crew = CrewRepository.get_by_id(db, data.crew_id)
        if not crew:
            raise HTTPException(
                status_code=404,
                detail="Crew not found",
            )

        # Check if availability already exists for this date
        existing = AvailabilityRepository.get_by_crew_and_date(
            db, data.crew_id, data.available_date
        )
        if existing:
            raise HTTPException(
                status_code=400,
                detail="Availability already exists for this crew and date",
            )

        availability = Availability(
            crew_id=data.crew_id,
            available_date=data.available_date,
            status=data.status,
            reason=data.reason,
        )

        return AvailabilityRepository.create(db, availability)

    @staticmethod
    def get_all_availabilities(db: Session, skip: int = 0, limit: int = 100):
        return AvailabilityRepository.get_by_date(
            db, date.today(), skip, limit
        )  # Default to today

    @staticmethod
    def get_availability(db: Session, availability_id: int):
        availability = AvailabilityRepository.get_by_id(db, availability_id)

        if not availability:
            raise HTTPException(
                status_code=404,
                detail="Availability not found",
            )

        return availability

    @staticmethod
    def update_availability(db: Session, availability_id: int, data: AvailabilityUpdate):
        availability = AvailabilityService.get_availability(db, availability_id)

        update_data = data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(availability, key, value)

        AvailabilityRepository.update(db)

        return availability

    @staticmethod
    def delete_availability(db: Session, availability_id: int):
        availability = AvailabilityService.get_availability(db, availability_id)
        AvailabilityRepository.delete(db, availability)

        return {"message": "Availability deleted successfully"}

    @staticmethod
    def get_crew_availability(db: Session, crew_id: int, skip: int = 0, limit: int = 100):
        crew = CrewRepository.get_by_id(db, crew_id)
        if not crew:
            raise HTTPException(
                status_code=404,
                detail="Crew not found",
            )

        return AvailabilityRepository.get_by_crew(db, crew_id, skip, limit)

    @staticmethod
    def get_availabilities_by_date(db: Session, availability_date: date, skip: int = 0, limit: int = 100):
        return AvailabilityRepository.get_by_date(db, availability_date, skip, limit)
