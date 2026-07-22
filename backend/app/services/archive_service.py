from typing import Any, Optional

from fastapi import HTTPException, Request
from sqlalchemy.orm import Session

from app.models.archive_data import ArchiveData
from app.models.main_data import MainData
from app.repositories.archive_repository import ArchiveRepository
from app.repositories.main_repository import MainRepository
from app.services.base_service import BaseService


class ArchiveService(BaseService[ArchiveData]):
    """
    Service for Archive module.

    Business Workflow (single transaction):
      1. Find MainData record
      2. Create ArchiveData snapshot from MainData
      3. Soft-delete MainData record (is_active = False)
      4. Audit Log
      5. Return ArchiveData
    """

    def __init__(self, db: Session, request: Optional[Request] = None):
        super().__init__(db)
        self.repo = ArchiveRepository(db)
        self.main_repo = MainRepository(db)
        self.model_class = ArchiveData
        self.entity_name = "ArchiveData"
        self.request = request

    def _meta(self) -> dict[str, Any]:
        ip = user_agent = None
        if self.request:
            ip = self.request.client.host if self.request.client else None
            user_agent = self.request.headers.get("user-agent")
        return {"ip_address": ip, "user_agent": user_agent}

    def archive_main_data(
        self,
        main_data_id: int,
        actor_username: str = "system",
    ) -> ArchiveData:
        """
        Archive a MainData record — create ArchiveData snapshot, then
        soft-delete the MainData row.
        """
        # 1. Find MainData record
        main = self.main_repo.get_by_id(main_data_id)
        if not main:
            raise HTTPException(status_code=404, detail="MainData record not found")
        if not main.is_active:
            raise HTTPException(status_code=400, detail="MainData record is already archived/inactive")

        old_value = {
            "main_data_id": main.id,
            "crew_id": main.crew_id,
            "train_no": main.train_no,
            "is_active": True,
        }

        # 2. Create ArchiveData snapshot
        archive = self.repo.create(
            signon_id=main.signon_id,
            crew_id=main.crew_id,
            crew_name=main.crew_name,
            train_no=main.train_no,
            from_station=main.from_station,
            to_station=main.to_station,
            status=main.status,
            sign_on_time=main.sign_on_time,
            cto_train_no=main.cto_train_no,
            cto_station=main.cto_station,
            cto_time=main.cto_time,
            loco1=main.loco1,
            loco2=main.loco2,
            loco3=main.loco3,
            shed=main.shed,
            is_active=False,
        )

        # 3. Soft-delete the MainData record
        self.main_repo.soft_delete(main)

        # 4. Audit Log
        self.log_audit(
            actor_username,
            "ARCHIVE",
            archive.id,
            old_value=old_value,
            new_value={"archive_id": archive.id, "is_active": False},
            **self._meta(),
        )

        self.db.flush()

        return archive

    def get_all_archive(
        self,
        skip: int = 0,
        limit: int = 100,
        crew_id: Optional[str] = None,
        search: Optional[str] = None,
        sort: str = "id",
        order: str = "asc",
    ):
        filters: dict[str, Any] = {}
        if crew_id is not None:
            filters["crew_id"] = crew_id

        search_fields = ["crew_id", "crew_name", "train_no"] if search else None

        items = self.repo.get_all(
            skip=skip,
            limit=limit,
            filters=filters,
            sort=sort,
            order=order,
            search=search,
            search_fields=search_fields,
        )
        total = self.repo.count(
            filters=filters,
            search=search,
            search_fields=search_fields,
        )
        page = (skip // limit) + 1 if limit else 1
        return self.paginated_response(items, total, page, limit)

