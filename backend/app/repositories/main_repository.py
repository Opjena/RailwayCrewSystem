from sqlalchemy.orm import Session
from typing import Optional, List

from app.models.main_data import MainData


class MainDataRepository:

    @staticmethod
    def get_by_id(db: Session, id: int) -> Optional[MainData]:
        return db.query(MainData).filter(MainData.id == id).first()

    @staticmethod
    def get_by_signon_id(db: Session, signon_id: int) -> Optional[MainData]:
        return (
            db.query(MainData)
            .filter(MainData.signon_id == signon_id, MainData.is_active == True)
            .first()
        )

    @staticmethod
    def get_by_crew_id(db: Session, crew_id: str) -> List[MainData]:
        return (
            db.query(MainData)
            .filter(MainData.crew_id == crew_id)
            .all()
        )

    @staticmethod
    def get_all(
        db: Session, skip: int = 0, limit: int = 100
    ) -> List[MainData]:
        return db.query(MainData).offset(skip).limit(limit).all()

    @staticmethod
    def create(db: Session, main_data: MainData) -> MainData:
        db.add(main_data)
        db.commit()
        db.refresh(main_data)
        return main_data

    @staticmethod
    def update(db: Session) -> None:
        db.commit()

    @staticmethod
    def delete(db: Session, main_data: MainData) -> None:
        db.delete(main_data)
        db.commit()
