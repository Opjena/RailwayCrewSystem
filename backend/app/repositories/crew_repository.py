from sqlalchemy.orm import Session

from app.models.crew import Crew


class CrewRepository:

    @staticmethod
    def get_by_id(db: Session, id: int):
        return db.query(Crew).filter(Crew.id == id).first()

    @staticmethod
    def get_by_crew_id(db: Session, crew_id: str):
        return db.query(Crew).filter(Crew.crew_id == crew_id).first()

    @staticmethod
    def get_by_mobile_number(db: Session, mobile_number: str):
        return db.query(Crew).filter(Crew.mobile_number == mobile_number).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Crew).offset(skip).limit(limit).all()

    @staticmethod
    def count_all(db: Session):
        return db.query(Crew).count()

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

