from fastapi import HTTPException, Request
from sqlalchemy.orm import Session
from typing import Optional, List

from app.models.main_data import MainData
from app.models.audit_log import AuditLog
from app.repositories.main_repository import MainDataRepository
from app.repositories.signon_repository import SignOnRepository
from app.schemas.main_data import CTOUpdate, ShedUpdate, LocoUpdate


class MainDataService:

    def __init__(self, db: Session, request: Optional[Request] = None):
        self.db = db
        self.request = request

    def _log_audit(
        self, action: str, entity_type: str, entity_id: int, actor: str, details: str = None
    ):
        log = AuditLog(
            action=action,
            entity=entity_type,
            entity_id=str(entity_id),
            actor_username=actor,
        )
        self.db.add(log)
        self.db.commit()

    def get_by_id_or_404(self, main_id: int) -> MainData:
        main = MainDataRepository.get_by_id(self.db, main_id)
        if not main:
            raise HTTPException(status_code=404, detail="MainData record not found")
        return main

    def create_from_signon(self, signon_id: int, actor_username: str) -> MainData:
        """Create MainData record from an existing SignOn record."""
        signon = SignOnRepository.get_by_id(self.db, signon_id)
        if not signon:
            raise HTTPException(status_code=404, detail="SignOn record not found")
        if not signon.is_active:
            raise HTTPException(status_code=400, detail="SignOn record is inactive")

        # Check if MainData already exists for this signon
        existing = MainDataRepository.get_by_signon_id(self.db, signon_id)
        if existing:
            raise HTTPException(
                status_code=400, detail="MainData already exists for this SignOn"
            )

        main_data = MainData(
            signon_id=signon.id,
            crew_id=signon.crew_id,
            crew_name=signon.crew_name,
            train_no=signon.train_no,
            from_station=signon.from_station,
            to_station=signon.to_station,
            status=signon.status,
            sign_on_time=signon.sign_on_time,
            cto_train_no=signon.cto_train_no,
            cto_station=signon.cto_station,
            cto_time=signon.cto_time,
            loco1=signon.loco1,
            loco2=signon.loco2,
            loco3=signon.loco3,
            shed=signon.shed,
        )
        created = MainDataRepository.create(self.db, main_data)

        self._log_audit(
            action="CREATE",
            entity_type="MainData",
            entity_id=created.id,
            actor=actor_username,
            details=f"MainData created from SignOn {signon_id} for crew {signon.crew_id}",
        )

        return created

    def update_cto(self, main_id: int, data: CTOUpdate, actor_username: str) -> MainData:
        main = self.get_by_id_or_404(main_id)
        main.cto_train_no = data.cto_train_no
        main.cto_station = data.cto_station
        main.cto_time = data.cto_time
        MainDataRepository.update(self.db)

        self._log_audit(
            action="CTO_UPDATE",
            entity_type="MainData",
            entity_id=main_id,
            actor=actor_username,
            details=f"CTO details updated for crew {main.crew_id}",
        )
        return main

    def update_shed(self, main_id: int, data: ShedUpdate, actor_username: str) -> MainData:
        main = self.get_by_id_or_404(main_id)
        main.shed = data.shed
        MainDataRepository.update(self.db)

        self._log_audit(
            action="SHED_UPDATE",
            entity_type="MainData",
            entity_id=main_id,
            actor=actor_username,
            details=f"Shed updated for crew {main.crew_id}",
        )
        return main

    def update_loco(self, main_id: int, data: LocoUpdate, actor_username: str) -> MainData:
        main = self.get_by_id_or_404(main_id)
        main.loco1 = data.loco1
        main.loco2 = data.loco2
        main.loco3 = data.loco3
        MainDataRepository.update(self.db)

        self._log_audit(
            action="LOCO_UPDATE",
            entity_type="MainData",
            entity_id=main_id,
            actor=actor_username,
            details=f"Locomotive details updated for crew {main.crew_id}",
        )
        return main

    def get_all_main_data(self, skip: int = 0, limit: int = 100) -> List[MainData]:
        return MainDataRepository.get_all(self.db, skip, limit)
