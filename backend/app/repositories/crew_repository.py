from typing import Optional

from sqlalchemy.orm import Session

from app.models.crew import Crew
from app.repositories.base_repository import BaseRepository


class CrewRepository(BaseRepository[Crew]):
    """Repository for Crew model — inherits generic CRUD from BaseRepository."""

    def __init__(self, db: Session):
        super().__init__(db, Crew)

    # ------------------------------------------------------------------
    # Crew-specific lookups
    # ------------------------------------------------------------------
    def get_by_crew_id(self, crew_id: str) -> Optional[Crew]:
        return self.db.query(Crew).filter(Crew.crew_id == crew_id).first()

    def get_by_mobile_number(self, mobile_number: str) -> Optional[Crew]:
        return self.db.query(Crew).filter(Crew.mobile_number == mobile_number).first()

