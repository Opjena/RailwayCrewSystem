from typing import Optional

from sqlalchemy.orm import Session

from app.models.main_data import MainData
from app.repositories.base_repository import BaseRepository


class MainRepository(BaseRepository[MainData]):
    """Repository for MainData model — inherits generic CRUD from BaseRepository."""

    def __init__(self, db: Session):
        super().__init__(db, MainData)

    def get_active_by_crew_id(self, crew_id: str) -> Optional[MainData]:
        return (
            self.db.query(MainData)
            .filter(MainData.crew_id == crew_id, MainData.is_active == True)
            .first()
        )

    def get_active_by_train(self, train_no: str) -> list[MainData]:
        return (
            self.db.query(MainData)
            .filter(MainData.train_no == train_no, MainData.is_active == True)
            .all()
        )

    def get_active_by_station(self, station: str) -> list[MainData]:
        return (
            self.db.query(MainData)
            .filter(
                (MainData.from_station == station) | (MainData.to_station == station),
                MainData.is_active == True,
            )
            .all()
        )

