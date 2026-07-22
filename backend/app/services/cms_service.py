from typing import Any, Optional

from fastapi import HTTPException, Request
from sqlalchemy.orm import Session

from app.models.cms_data import CMSData
from app.repositories.cms_repository import CMSRepository
from app.schemas.cms_data import CMSDataCreate, CMSDataUpdate
from app.services.base_service import BaseService


class CMSService(BaseService[CMSData]):
    """Service for CMS module — inherits common CRUD from BaseService."""

    def __init__(self, db: Session, request: Optional[Request] = None):
        super().__init__(db)
        self.repo = CMSRepository(db)
        self.model_class = CMSData
        self.entity_name = "CMSData"
        self.request = request

    # ── helper to extract request metadata ────────────────────────────
    def _meta(self) -> dict[str, Any]:
        ip = user_agent = None
        if self.request:
            ip = self.request.client.host if self.request.client else None
            user_agent = self.request.headers.get("user-agent")
        return {"ip_address": ip, "user_agent": user_agent}

    # ── CREATE ────────────────────────────────────────────────────────
    def create_cms(self, data: CMSDataCreate, actor_username: str = "system") -> CMSData:
        # Duplicate check: prevent same crew_id + train_no + status combination
        filters = {
            "crew_id": data.crew_id,
            "train_no": data.train_no,
            "is_active": True,
        }
        existing = self.repo.get_all(filters=filters, limit=1)
        if existing:
            raise HTTPException(
                status_code=400,
                detail="Active CMS record already exists for this crew and train",
            )

        cms = self.repo.create(
            crew_id=data.crew_id,
            crew_name=data.crew_name,
            crew_designation=data.crew_designation,
            fortnight_hours=data.fortnight_hours,
            avail_time=data.avail_time,
            avail_station=data.avail_station,
            status=data.status,
            called_time=data.called_time,
            ack_time=data.ack_time,
            sign_on_time=data.sign_on_time,
            last_signoff_time=data.last_signoff_time,
            train_no=data.train_no,
            from_station=data.from_station,
            to_station=data.to_station,
            is_active=True,
            is_imported=False,
        )

        self.log_audit(
            actor_username,
            "CREATE",
            cms.id,
            new_value={"crew_id": cms.crew_id, "train_no": cms.train_no},
            **self._meta(),
        )
        return cms

    # ── READ ──────────────────────────────────────────────────────────
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
    ):
        filters: dict[str, Any] = {}
        if crew_id is not None:
            filters["crew_id"] = crew_id
        if status is not None:
            filters["status"] = status
        if is_active is not None:
            filters["is_active"] = is_active

        search_fields = ["crew_id", "crew_name", "train_no", "from_station", "to_station"] if search else None

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

    # ── UPDATE ────────────────────────────────────────────────────────
    def update_cms(
        self,
        cms_id: int,
        data: CMSDataUpdate,
        actor_username: str = "system",
    ) -> CMSData:
        cms = self.get_by_id_or_404(cms_id)
        update_data = data.model_dump(exclude_unset=True)
        old = {k: getattr(cms, k) for k in update_data if hasattr(cms, k)}

        for key, value in update_data.items():
            setattr(cms, key, value)
        self.repo.update(cms)

        self.log_audit(
            actor_username,
            "UPDATE",
            cms.id,
            old_value=old,
            new_value=update_data,
            **self._meta(),
        )
        return cms

    # ── SOFT DELETE ───────────────────────────────────────────────────
    def delete_cms(self, cms_id: int, actor_username: str = "system") -> dict:
        cms = self.get_by_id_or_404(cms_id)
        self.repo.soft_delete(cms)

        self.log_audit(
            actor_username,
            "DEACTIVATE",
            cms.id,
            old_value={"is_active": True},
            new_value={"is_active": False},
            **self._meta(),
        )
        return {"message": "CMS record deactivated successfully"}

