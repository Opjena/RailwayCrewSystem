from typing import Optional

from sqlalchemy.orm import Session

from app.models.cms_data import CMSData
from app.repositories.base_repository import BaseRepository


class CMSRepository(BaseRepository[CMSData]):
    """Repository for CMSData model — inherits generic CRUD from BaseRepository."""

    def __init__(self, db: Session):
        super().__init__(db, CMSData)

    def get_by_crew_id(self, crew_id: str) -> Optional[CMSData]:
        return self.db.query(CMSData).filter(CMSData.crew_id == crew_id).first()

    def get_active_by_crew_id(self, crew_id: str) -> Optional[CMSData]:
        return (
            self.db.query(CMSData)
            .filter(CMSData.crew_id == crew_id, CMSData.is_active == True)
            .first()
        )

