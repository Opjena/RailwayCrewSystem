from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.auth.hashing import hash_password
from app.models.crew import Crew
from app.repositories.crew_repository import CrewRepository
from app.schemas.crew import CrewCreate, CrewUpdate, CrewListResponse


class CrewService:

    @staticmethod
    def create_crew(db: Session, data: CrewCreate):
        # Validate duplicate crew_id
        if CrewRepository.get_by_crew_id(db, data.crew_id):
            raise HTTPException(
                status_code=400,
                detail="Crew ID already exists",
            )

        # Validate duplicate mobile_number
        if CrewRepository.get_by_mobile_number(db, data.mobile_number):
            raise HTTPException(
                status_code=400,
                detail="Mobile number already exists",
            )

        crew = Crew(
            crew_id=data.crew_id,
            full_name=data.full_name,
            department=data.department,
            mobile_number=data.mobile_number,
            designation=data.designation,
            password_hash=hash_password(data.password),
            is_active=True,
        )

        return CrewRepository.create(db, crew)

    @staticmethod
    def get_crew_by_crew_id(db: Session, crew_id: str):
        crew = CrewRepository.get_by_crew_id(db, crew_id)

        if not crew:
            raise HTTPException(
                status_code=404,
                detail="Crew not found",
            )

        return crew

    @staticmethod
    def get_all_crew(db: Session, skip: int = 0, limit: int = 100):
        items = CrewRepository.get_all(db, skip, limit)
        total = CrewRepository.count_all(db)

        return CrewListResponse(total=total, items=items)

    @staticmethod
    def update_crew(db: Session, crew_id: str, data: CrewUpdate):
        crew = CrewService.get_crew_by_crew_id(db, crew_id)

        # If mobile_number is being updated, check for duplicates
        if data.mobile_number and data.mobile_number != crew.mobile_number:
            if CrewRepository.get_by_mobile_number(db, data.mobile_number):
                raise HTTPException(
                    status_code=400,
                    detail="Mobile number already exists",
                )

        update_data = data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(crew, key, value)

        CrewRepository.update(db)

        return crew

    @staticmethod
    def delete_crew(db: Session, crew_id: str):
        crew = CrewService.get_crew_by_crew_id(db, crew_id)
        CrewRepository.delete(db, crew)

        return {"message": "Crew deleted successfully"}

