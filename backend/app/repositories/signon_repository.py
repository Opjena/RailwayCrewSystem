from typing import Optional

from sqlalchemy.orm import Session

from app.models.signon_data import SignOnData
from app.repositories.base_repository import BaseRepository


class SignOnRepository(BaseRepository[SignOnData]):
    """Repository for SignOnData model — inherits generic CRUD from BaseRepository."""

    def __init__(self, db: Session):
        super().__init__(db, SignOnData)

    def get_by_crew_id(self, crew_id: str) -> list[SignOnData]:
        return self.db.query(SignOnData).filter(SignOnData.crew_id == crew_id).all()

    def get_active_by_cms_id(self, cms_id: int) -> Optional[SignOnData]:
        return (
            self.db.query(SignOnData)
            .filter(SignOnData.cms_id == cms_id, SignOnData.is_active == True)
            .first()
        )

