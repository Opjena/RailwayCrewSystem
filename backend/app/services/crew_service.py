from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.crew import Crew
from app.repositories.crew_repository import CrewRepository
from app.schemas.crew import CrewCreate, CrewUpdate


class CrewService:

    @staticmethod
    def create_crew(db: Session, data: CrewCreate):
        # Check if crew_id already exists
        if CrewRepository.get_by_crew_id(db, data.crew_id):
            raise HTTPException(
                status_code=400,
                detail="Crew ID already exists",
            )

        # Check if email already exists
        if CrewRepository.get_by_email(db, data.email):
            raise HTTPException(
                status_code=400,
                detail="Email already exists",
            )

        crew = Crew(
            crew_id=data.crew_id,
            full_name=data.full_name,
            department=data.department,
            email=data.email,
            phone=data.phone,
            is_active=True,
        )

        return CrewRepository.create(db, crew)

    @staticmethod
    def get_all_crew(db: Session, skip: int = 0, limit: int = 100):
        return CrewRepository.get_all(db, skip, limit)

    @staticmethod
    def get_crew(db: Session, crew_id: int):
        crew = CrewRepository.get_by_id(db, crew_id)

        if not crew:
            raise HTTPException(
                status_code=404,
                detail="Crew not found",
            )

        return crew

    @staticmethod
    def update_crew(db: Session, crew_id: int, data: CrewUpdate):
        crew = CrewService.get_crew(db, crew_id)

        # Check if new email is already used by another crew
        if data.email and data.email != crew.email:
            if CrewRepository.get_by_email(db, data.email):
                raise HTTPException(
                    status_code=400,
                    detail="Email already exists",
                )

        update_data = data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(crew, key, value)

        CrewRepository.update(db)

        return crew

    @staticmethod
    def delete_crew(db: Session, crew_id: int):
        crew = CrewService.get_crew(db, crew_id)
        CrewRepository.delete(db, crew)

        return {"message": "Crew deleted successfully"}

    @staticmethod
    def get_crew_by_department(db: Session, department: str, skip: int = 0, limit: int = 100):
        from app.core.enums import Department

        try:
            dept_enum = Department[department.upper()]
        except KeyError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid department. Valid options: {[d.name for d in Department]}",
            )

        return CrewRepository.get_by_department(db, dept_enum, skip, limit)

    @staticmethod
    def get_active_crew(db: Session, skip: int = 0, limit: int = 100):
        return CrewRepository.get_active(db, skip, limit)
