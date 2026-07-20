from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.shift import Shift
from app.core.enums import ShiftType
from datetime import date


class ShiftRepository:

    @staticmethod
    def get_by_id(db: Session, shift_id: int):
        return db.query(Shift).filter(Shift.id == shift_id).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Shift).offset(skip).limit(limit).all()

    @staticmethod
    def get_by_date(db: Session, shift_date: date, skip: int = 0, limit: int = 100):
        return (
            db.query(Shift)
            .filter(Shift.shift_date == shift_date)
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_by_date_range(db: Session, start_date: date, end_date: date):
        return (
            db.query(Shift)
            .filter(and_(Shift.shift_date >= start_date, Shift.shift_date <= end_date))
            .order_by(Shift.shift_date)
            .all()
        )

    @staticmethod
    def get_by_type(db: Session, shift_type: ShiftType, skip: int = 0, limit: int = 100):
        return (
            db.query(Shift)
            .filter(Shift.shift_type == shift_type)
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def create(db: Session, shift: Shift):
        db.add(shift)
        db.commit()
        db.refresh(shift)
        return shift

    @staticmethod
    def update(db: Session):
        db.commit()

    @staticmethod
    def delete(db: Session, shift: Shift):
        db.delete(shift)
        db.commit()
