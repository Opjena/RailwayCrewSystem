from sqlalchemy.orm import Session
from app.models.crew import Crew
from app.core.enums import Department


class CrewRepository:

    @staticmethod
    def get_by_id(db: Session, crew_id: int):
        return db.query(Crew).filter(Crew.id == crew_id).first()

    @staticmethod
    def get_by_crew_id(db: Session, crew_id: str):
        return db.query(Crew).filter(Crew.crew_id == crew_id).first()

    @staticmethod
    def get_by_email(db: Session, email: str):
        return db.query(Crew).filter(Crew.email == email).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Crew).offset(skip).limit(limit).all()

    @staticmethod
    def get_by_department(db: Session, department: Department, skip: int = 0, limit: int = 100):
        return (
            db.query(Crew)
            .filter(Crew.department == department)
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_active(db: Session, skip: int = 0, limit: int = 100):
        return (
            db.query(Crew)
            .filter(Crew.is_active == True)
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def create(db: Session, crew: Crew):
        db.add(crew)
        db.commit()
        db.refresh(crew)
        return crew

    @staticmethod
    def update(db: Session):
        db.commit()

    @staticmethod
    def delete(db: Session, crew: Crew):
        db.delete(crew)
        db.commit()
