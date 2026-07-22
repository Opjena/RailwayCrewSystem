from fastapi import HTTPException, Request
from sqlalchemy.orm import Session
from typing import Optional, List

from app.models.signon_data import SignOnData
from app.models.audit_log import AuditLog
from app.repositories.signon_repository import SignOnRepository
from app.repositories.cms_repository import CMSRepository
from app.schemas.signon_data import SignOnDataCreate, SignOnDataUpdate


class SignOnService:

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

    def get_by_id_or_404(self, signon_id: int) -> SignOnData:
        signon = SignOnRepository.get_by_id(self.db, signon_id)
        if not signon:
            raise HTTPException(status_code=404, detail="SignOn record not found")
        return signon

    def create_signon(self, data: SignOnDataCreate, actor_username: str) -> SignOnData:
        # Verify CMS record exists
        cms = CMSRepository.get_by_id(self.db, data.cms_id)
        if not cms:
            raise HTTPException(status_code=404, detail="CMS record not found")

        # Check for duplicate active signon
        existing = SignOnRepository.get_active_by_crew_and_train(
            self.db, data.crew_id, data.train_no
        )
        if existing:
            raise HTTPException(
                status_code=400,
                detail=f"Active SignOn already exists for crew {data.crew_id} on train {data.train_no}",
            )

        signon = SignOnData(**data.model_dump())
        created = SignOnRepository.create(self.db, signon)

        # Update CMS status
        cms.status = "SIGNED_ON"
        CMSRepository.update(self.db)

        self._log_audit(
            action="CREATE",
            entity_type="SignOn",
            entity_id=created.id,
            actor=actor_username,
            details=f"SignOn created for crew {data.crew_id} on train {data.train_no}",
        )

        return created

    def get_all_signon(self, skip: int = 0, limit: int = 100) -> List[SignOnData]:
        return SignOnRepository.get_all(self.db, skip, limit)

    def update_signon(
        self, signon_id: int, data: SignOnDataUpdate, actor_username: str
    ) -> SignOnData:
        signon = self.get_by_id_or_404(signon_id)

        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(signon, key, value)

        SignOnRepository.update(self.db)

        self._log_audit(
            action="UPDATE",
            entity_type="SignOn",
            entity_id=signon_id,
            actor=actor_username,
            details=f"SignOn updated for crew {signon.crew_id}",
        )

        return signon

    def delete_signon(self, signon_id: int, actor_username: str) -> dict:
        signon = self.get_by_id_or_404(signon_id)
        signon.is_active = False
        SignOnRepository.update(self.db)

        self._log_audit(
            action="DEACTIVATE",
            entity_type="SignOn",
            entity_id=signon_id,
            actor=actor_username,
            details=f"SignOn deactivated for crew {signon.crew_id}",
        )

        return {"message": "SignOn record deactivated successfully"}
