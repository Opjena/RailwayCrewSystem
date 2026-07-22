from fastapi import HTTPException, Request
from sqlalchemy.orm import Session
from typing import Optional, List

from app.models.archive_data import ArchiveData
from app.models.audit_log import AuditLog
from app.repositories.archive_repository import ArchiveRepository
from app.repositories.main_repository import MainDataRepository
from app.repositories.signon_repository import SignOnRepository


class ArchiveService:

    def __init__(self, db: Session, request: Optional[Request] = None):
        self.db = db
        self.request = request

    def _log_audit(
        self, action: str, entity_type: str, entity_id: int, actor: str, details: str = None
    ):
        log = AuditLog(
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            user_id=actor,
            details=details,
            ip_address=self.request.client.host if self.request else None,
        )
        self.db.add(log)
        self.db.commit()

    def get_by_id_or_404(self, archive_id: int) -> ArchiveData:
        archive = ArchiveRepository.get_by_id(self.db, archive_id)
        if not archive:
            raise HTTPException(status_code=404, detail="Archive record not found")
        return archive

    def archive_from_main(self, main_id: int, actor_username: str) -> ArchiveData:
        """Archive a MainData record by moving it to archive."""
        main = MainDataRepository.get_by_id(self.db, main_id)
        if not main:
            raise HTTPException(status_code=404, detail="MainData record not found")

        # Check if already archived
        existing = ArchiveRepository.get_by_signon_id(self.db, main.signon_id)
        if existing:
            raise HTTPException(
                status_code=400, detail="This record has already been archived"
            )

        archive = ArchiveData(
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
            is_active=True,
        )
        created = ArchiveRepository.create(self.db, archive)

        # Mark MainData as inactive
        main.is_active = False
        MainDataRepository.update(self.db)

        # Also mark SignOn as inactive
        signon = SignOnRepository.get_by_id(self.db, main.signon_id)
        if signon:
            signon.is_active = False
            SignOnRepository.update(self.db)

        self._log_audit(
            action="ARCHIVE",
            entity_type="Archive",
            entity_id=created.id,
            actor=actor_username,
            details=f"Record archived for crew {main.crew_id} from MainData {main_id}",
        )

        return created

    def get_all_archived(
        self, skip: int = 0, limit: int = 100
    ) -> List[ArchiveData]:
        return ArchiveRepository.get_all(self.db, skip, limit)
