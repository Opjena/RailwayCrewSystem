from sqlalchemy.orm import Session

from app.models.archive_data import ArchiveData
from app.repositories.base_repository import BaseRepository


class ArchiveRepository(BaseRepository[ArchiveData]):
    """Repository for ArchiveData model — inherits generic CRUD from BaseRepository."""

    def __init__(self, db: Session):
        super().__init__(db, ArchiveData)

