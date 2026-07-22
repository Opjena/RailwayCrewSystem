from sqlalchemy.orm import Session
from typing import Optional, List

from app.models.signon_data import SignOnData


class SignOnRepository:

    @staticmethod
    def get_by_id(db: Session, id: int) -> Optional[SignOnData]:
        return db.query(SignOnData).filter(SignOnData.id == id).first()

    @staticmethod
    def get_by_crew_id(db: Session, crew_id: str) -> List[SignOnData]:
        return (
            db.query(SignOnData)
            .filter(SignOnData.crew_id == crew_id)
            .all()
        )

    @staticmethod
    def get_by_cms_id(db: Session, cms_id: int) -> Optional[SignOnData]:
        return (
            db.query(SignOnData)
            .filter(SignOnData.cms_id == cms_id, SignOnData.is_active == True)
            .first()
        )

    @staticmethod
    def get_active_by_crew_and_train(
        db: Session, crew_id: str, train_no: str
    ) -> Optional[SignOnData]:
        return (
            db.query(SignOnData)
            .filter(
                SignOnData.crew_id == crew_id,
                SignOnData.train_no == train_no,
                SignOnData.is_active == True,
            )
            .first()
        )

    @staticmethod
    def get_all(
        db: Session, skip: int = 0, limit: int = 100
    ) -> List[SignOnData]:
        return db.query(SignOnData).offset(skip).limit(limit).all()

    @staticmethod
    def create(db: Session, signon: SignOnData) -> SignOnData:
        db.add(signon)
        db.commit()
        db.refresh(signon)
        return signon

    @staticmethod
    def update(db: Session) -> None:
        db.commit()

    @staticmethod
    def delete(db: Session, signon: SignOnData) -> None:
        db.delete(signon)
        db.commit()
