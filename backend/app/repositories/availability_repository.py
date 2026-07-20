from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.availability import Availability
from app.core.enums import AvailabilityStatus
from datetime import date


class AvailabilityRepository:

    @staticmethod
    def get_by_id(db: Session, availability_id: int):
        return db.query(Availability).filter(Availability.id == availability_id).first()

    @staticmethod
    def get_by_crew(db: Session, crew_id: int, skip: int = 0, limit: int = 100):
        return (
            db.query(Availability)
            .filter(Availability.crew_id == crew_id)
            .order_by(Availability.available_date.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_by_crew_and_date(db: Session, crew_id: int, available_date: date):
        return (
            db.query(Availability)
            .filter(and_(Availability.crew_id == crew_id, Availability.available_date == available_date))
            .first()
        )

    @staticmethod
    def get_by_date(db: Session, available_date: date, skip: int = 0, limit: int = 100):
        return (
            db.query(Availability)
            .filter(Availability.available_date == available_date)
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_by_date_range(db: Session, start_date: date, end_date: date, crew_id: int = None):
        query = db.query(Availability).filter(
            and_(Availability.available_date >= start_date, Availability.available_date <= end_date)
        )
        if crew_id:
            query = query.filter(Availability.crew_id == crew_id)
        return query.order_by(Availability.available_date).all()

    @staticmethod
    def get_by_status(db: Session, status: AvailabilityStatus, skip: int = 0, limit: int = 100):
        return (
            db.query(Availability)
            .filter(Availability.status == status)
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def create(db: Session, availability: Availability):
        db.add(availability)
        db.commit()
        db.refresh(availability)
        return availability

    @staticmethod
    def update(db: Session):
        db.commit()

    @staticmethod
    def delete(db: Session, availability: Availability):
        db.delete(availability)
        db.commit()
