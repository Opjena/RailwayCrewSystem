from sqlalchemy.orm import Session
from typing import Optional, List

from app.models.archive_data import ArchiveData


class ArchiveRepository:

    @staticmethod
    def get_by_id(db: Session, id: int) -> Optional[ArchiveData]:
        return db.query(ArchiveData).filter(ArchiveData.id == id).first()

    @staticmethod
    def get_by_signon_id(db: Session, signon_id: int) -> Optional[ArchiveData]:
        return (
            db.query(ArchiveData)
            .filter(ArchiveData.signon_id == signon_id)
            .first()
        )

    @staticmethod
    def get_by_crew_id(db: Session, crew_id: str) -> List[ArchiveData]:
        return (
            db.query(ArchiveData)
            .filter(ArchiveData.crew_id == crew_id)
            .all()
        )

    @staticmethod
    def get_all(
        db: Session, skip: int = 0, limit: int = 100
    ) -> List[ArchiveData]:
        return db.query(ArchiveData).offset(skip).limit(limit).all()

    @staticmethod
    def create(db: Session, archive: ArchiveData) -> ArchiveData:
        db.add(archive)
        db.commit()
        db.refresh(archive)
        return archive

    @staticmethod
    def update(db: Session) -> None:
        db.commit()

    @staticmethod
    def delete(db: Session, archive: ArchiveData) -> None:
        db.delete(archive)
        db.commit()
