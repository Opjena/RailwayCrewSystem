from typing import Any, Optional

from fastapi import HTTPException, Request
from sqlalchemy.orm import Session

from app.models.signon_data import SignOnData
from app.models.main_data import MainData
from app.repositories.signon_repository import SignOnRepository
from app.repositories.cms_repository import CMSRepository
from app.repositories.main_repository import MainRepository
from app.repositories.crew_repository import CrewRepository
from app.schemas.signon_data import SignOnDataCreate, SignOnDataUpdate
from app.services.base_service import BaseService


class SignOnService(BaseService[SignOnData]):
    """
    Service for SignOn module.

    Business Workflow (single transaction):
      1. Find Crew exists
      2. Find CMS record exists and is active
      3. Validate no duplicate active SignOn for this CMS
      4. Create SignOn
      5. Create MainData from the SignOn snapshot
      6. Audit Log
      7. Return SignOn + MainData
    """

    def __init__(self, db: Session, request: Optional[Request] = None):
        super().__init__(db)
        self.repo = SignOnRepository(db)
        self.cms_repo = CMSRepository(db)
        self.main_repo = MainRepository(db)
        self.crew_repo = CrewRepository(db)
        self.model_class = SignOnData
        self.entity_name = "SignOnData"
        self.request = request

    def _meta(self) -> dict[str, Any]:
        ip = user_agent = None
        if self.request:
            ip = self.request.client.host if self.request.client else None
            user_agent = self.request.headers.get("user-agent")
        return {"ip_address": ip, "user_agent": user_agent}

    # ── CREATE (with MainData creation in one transaction) ────────────
    def create_signon(
        self,
        data: SignOnDataCreate,
        actor_username: str = "system",
    ) -> dict:
        # 1. Verify Crew exists in master
        crew = self.crew_repo.get_by_crew_id(data.crew_id)
        if not crew:
            raise HTTPException(status_code=404, detail="Crew not found in master data")
        if not crew.is_active:
            raise HTTPException(status_code=400, detail="Crew is inactive")

        # 2. Verify CMS record exists and is active
        cms = self.cms_repo.get_by_id(data.cms_id)
        if not cms:
            raise HTTPException(status_code=404, detail="CMS record not found")
        if not cms.is_active:
            raise HTTPException(status_code=400, detail="CMS record is not active")

        # 3. Check no duplicate active SignOn for this CMS
        existing = self.repo.get_active_by_cms_id(data.cms_id)
        if existing:
            raise HTTPException(
                status_code=400,
                detail="An active SignOn already exists for this CMS record",
            )

        # 4. Create SignOn
        signon = self.repo.create(
            cms_id=data.cms_id,
            crew_id=data.crew_id,
            crew_name=data.crew_name,
            status=data.status,
            train_no=data.train_no,
            from_station=data.from_station,
            to_station=data.to_station,
            sign_on_time=data.sign_on_time,
            cto_train_no=data.cto_train_no,
            cto_station=data.cto_station,
            cto_time=data.cto_time,
            loco1=data.loco1,
            loco2=data.loco2,
            loco3=data.loco3,
            shed=data.shed,
            is_active=True,
        )

        # 5. Create MainData from SignOn snapshot
        main_data = self.main_repo.create(
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
            is_active=True,
        )

        # 6. Audit Log
        self.log_audit(
            actor_username,
            "CREATE",
            signon.id,
            new_value={
                "signon_id": signon.id,
                "main_data_id": main_data.id,
                "crew_id": signon.crew_id,
                "train_no": signon.train_no,
            },
            **self._meta(),
        )

        self.db.flush()

        return {
            "signon": signon,
            "main_data": main_data,
        }

    # ── READ ──────────────────────────────────────────────────────────
    def get_all_signon(
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

    # ── UPDATE ────────────────────────────────────────────────────────
    def update_signon(
        self,
        signon_id: int,
        data: SignOnDataUpdate,
        actor_username: str = "system",
    ) -> SignOnData:
        signon = self.get_by_id_or_404(signon_id)
        update_data = data.model_dump(exclude_unset=True)
        old = {k: getattr(signon, k) for k in update_data if hasattr(signon, k)}

        for key, value in update_data.items():
            setattr(signon, key, value)
        self.repo.update(signon)

        self.log_audit(
            actor_username,
            "UPDATE",
            signon.id,
            old_value=old,
            new_value=update_data,
            **self._meta(),
        )
        return signon

    # ── SOFT DELETE ───────────────────────────────────────────────────
    def delete_signon(self, signon_id: int, actor_username: str = "system") -> dict:
        signon = self.get_by_id_or_404(signon_id)
        self.repo.soft_delete(signon)

        self.log_audit(
            actor_username,
            "DEACTIVATE",
            signon.id,
            old_value={"is_active": True},
            new_value={"is_active": False},
            **self._meta(),
        )
        return {"message": "SignOn record deactivated successfully"}

