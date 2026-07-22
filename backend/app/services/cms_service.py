from fastapi import HTTPException, Request
from sqlalchemy.orm import Session
from typing import Optional

from app.models.cms_data import CMSData
from app.models.audit_log import AuditLog
from app.repositories.cms_repository import CMSRepository
from app.schemas.cms_data import CMSDataCreate, CMSDataUpdate


class CMSService:

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

    def get_by_id_or_404(self, cms_id: int) -> CMSData:
        cms = CMSRepository.get_by_id(self.db, cms_id)
        if not cms:
            raise HTTPException(status_code=404, detail="CMS record not found")
        return cms

    def create_cms(self, data: CMSDataCreate, actor_username: str) -> CMSData:
        # Check for duplicate crew_id
        existing = CMSRepository.get_by_crew_id(self.db, data.crew_id)
        if existing and existing.is_active:
            raise HTTPException(
                status_code=400,
                detail=f"CMS record for crew {data.crew_id} already exists",
            )

        cms = CMSData(**data.model_dump())
        created = CMSRepository.create(self.db, cms)

        self._log_audit(
            action="CREATE",
            entity_type="CMS",
            entity_id=created.id,
            actor=actor_username,
            details=f"CMS record created for crew {data.crew_id}",
        )

        return created

    def get_all_cms(
        self,
        skip: int = 0,
        limit: int = 100,
        crew_id: Optional[str] = None,
        status: Optional[str] = None,
        is_active: Optional[bool] = None,
        search: Optional[str] = None,
        sort: str = "id",
        order: str = "asc",
    ) -> dict:
        items, total = CMSRepository.get_all(
            self.db,
            skip=skip,
            limit=limit,
            crew_id=crew_id,
            status=status,
            is_active=is_active,
            search=search,
            sort=sort,
            order=order,
        )
        return {
            "items": items,
            "total": total,
            "page": skip // limit + 1 if limit else 1,
            "page_size": limit,
            "total_pages": (total + limit - 1) // limit if limit else 1,
        }

    def update_cms(self, cms_id: int, data: CMSDataUpdate, actor_username: str) -> CMSData:
        cms = self.get_by_id_or_404(cms_id)

        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(cms, key, value)

        CMSRepository.update(self.db)

        self._log_audit(
            action="UPDATE",
            entity_type="CMS",
            entity_id=cms_id,
            actor=actor_username,
            details=f"CMS record updated for crew {cms.crew_id}",
        )

        return cms

    def delete_cms(self, cms_id: int, actor_username: str) -> dict:
        cms = self.get_by_id_or_404(cms_id)
        cms.is_active = False
        CMSRepository.update(self.db)

        self._log_audit(
            action="DEACTIVATE",
            entity_type="CMS",
            entity_id=cms_id,
            actor=actor_username,
            details=f"CMS record deactivated for crew {cms.crew_id}",
        )

        return {"message": "CMS record deactivated successfully"}
