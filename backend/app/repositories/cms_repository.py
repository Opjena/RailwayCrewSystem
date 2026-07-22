from sqlalchemy.orm import Session
from typing import Optional, List

from app.models.cms_data import CMSData


class CMSRepository:

    @staticmethod
    def get_by_id(db: Session, cms_id: int) -> Optional[CMSData]:
        return db.query(CMSData).filter(CMSData.id == cms_id).first()

    @staticmethod
    def get_by_crew_id(db: Session, crew_id: str) -> Optional[CMSData]:
        return (
            db.query(CMSData)
            .filter(CMSData.crew_id == crew_id, CMSData.is_active == True)
            .first()
        )

    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        crew_id: Optional[str] = None,
        status: Optional[str] = None,
        is_active: Optional[bool] = None,
        search: Optional[str] = None,
        sort: str = "id",
        order: str = "asc",
    ) -> tuple[List[CMSData], int]:
        query = db.query(CMSData)

        if crew_id:
            query = query.filter(CMSData.crew_id == crew_id)
        if status:
            query = query.filter(CMSData.status == status)
        if is_active is not None:
            query = query.filter(CMSData.is_active == is_active)
        if search:
            query = query.filter(
                CMSData.crew_name.ilike(f"%{search}%")
                | CMSData.crew_id.ilike(f"%{search}%")
            )

        total = query.count()

        sort_col = getattr(CMSData, sort, CMSData.id)
        if order == "desc":
            sort_col = sort_col.desc()
        query = query.order_by(sort_col).offset(skip).limit(limit)

        return query.all(), total

    @staticmethod
    def create(db: Session, cms: CMSData) -> CMSData:
        db.add(cms)
        db.commit()
        db.refresh(cms)
        return cms

    @staticmethod
    def update(db: Session) -> None:
        db.commit()

    @staticmethod
    def delete(db: Session, cms: CMSData) -> None:
        db.delete(cms)
        db.commit()
