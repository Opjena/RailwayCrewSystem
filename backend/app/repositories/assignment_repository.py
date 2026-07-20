from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.assignment import Assignment
from app.core.enums import AssignmentStatus


class AssignmentRepository:

    @staticmethod
    def get_by_id(db: Session, assignment_id: int):
        return db.query(Assignment).filter(Assignment.id == assignment_id).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Assignment).offset(skip).limit(limit).all()

    @staticmethod
    def get_by_shift(db: Session, shift_id: int):
        return db.query(Assignment).filter(Assignment.shift_id == shift_id).all()

    @staticmethod
    def get_by_crew(db: Session, crew_id: int, skip: int = 0, limit: int = 100):
        return (
            db.query(Assignment)
            .filter(Assignment.crew_id == crew_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_by_status(db: Session, status: AssignmentStatus, skip: int = 0, limit: int = 100):
        return (
            db.query(Assignment)
            .filter(Assignment.status == status)
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_by_shift_and_crew(db: Session, shift_id: int, crew_id: int):
        return (
            db.query(Assignment)
            .filter(and_(Assignment.shift_id == shift_id, Assignment.crew_id == crew_id))
            .first()
        )

    @staticmethod
    def create(db: Session, assignment: Assignment):
        db.add(assignment)
        db.commit()
        db.refresh(assignment)
        return assignment

    @staticmethod
    def update(db: Session):
        db.commit()

    @staticmethod
    def delete(db: Session, assignment: Assignment):
        db.delete(assignment)
        db.commit()
