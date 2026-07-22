from typing import Any, Optional

from fastapi import HTTPException, Request
from sqlalchemy.orm import Session

from app.models.main_data import MainData
from app.repositories.main_repository import MainRepository
from app.schemas.main_data import CTOUpdate, ShedUpdate, LocoUpdate
from app.services.base_service import BaseService


class MainService(BaseService[MainData]):
    """
    Service for MainData module — used primarily for the Dashboard.

    Provides:
      - Active crew queries (by train, station, crew)
      - CTO / Shed / Loco updates
      - Audit logging for all mutations
    """

    def __init__(self, db: Session, request: Optional[Request] = None):
        super().__init__(db)
        self.repo = MainRepository(db)
        self.model_class = MainData
        self.entity_name = "MainData"
        self.request = request

    def _meta(self) -> dict[str, Any]:
        ip = user_agent = None
        if self.request:
            ip = self.request.client.host if self.request.client else None
            user_agent = self.request.headers.get("user-agent")
        return {"ip_address": ip, "user_agent": user_agent}

    # ── READ ──────────────────────────────────────────────────────────
    def get_all_main(
        self,
        skip: int = 0,
        limit: int = 100,
        crew_id: Optional[str] = None,
        train_no: Optional[str] = None,
        station: Optional[str] = None,
        status: Optional[str] = None,
        is_active: Optional[bool] = None,
        search: Optional[str] = None,
        sort: str = "id",
        order: str = "asc",
    ):
        filters: dict[str, Any] = {}
        if crew_id is not None:
            filters["crew_id"] = crew_id
        if train_no is not None:
            filters["train_no"] = train_no
        if status is not None:
            filters["status"] = status
        if is_active is not None:
            filters["is_active"] = is_active

        # Station filter is an OR condition handled separately
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

    def get_active_crew(self, skip: int = 0, limit: int = 100):
        """Get all currently active (signed-on) crew."""
        return self.get_all_main(skip=skip, limit=limit, is_active=True)

    def get_by_train(self, train_no: str):
        """Get all active crew assigned to a train."""
        items = self.repo.get_active_by_train(train_no)
        total = len(items)
        return self.paginated_response(items, total, 1, total if total else 1)

    def get_by_station(self, station: str):
        """Get active crew at a station (from or to)."""
        items = self.repo.get_active_by_station(station)
        total = len(items)
        return self.paginated_response(items, total, 1, total if total else 1)

    def get_by_crew(self, crew_id: str):
        """Get active record for a specific crew."""
        main = self.repo.get_active_by_crew_id(crew_id)
        if not main:
            raise HTTPException(status_code=404, detail="No active record found for this crew")
        return main

    # ── CTO UPDATE ────────────────────────────────────────────────────
    def update_cto(
        self,
        main_id: int,
        data: CTOUpdate,
        actor_username: str = "system",
    ) -> MainData:
        main = self.get_by_id_or_404(main_id)
        old = {
            "cto_train_no": main.cto_train_no,
            "cto_station": main.cto_station,
            "cto_time": main.cto_time,
        }
        main.cto_train_no = data.cto_train_no
        main.cto_station = data.cto_station
        main.cto_time = data.cto_time
        self.repo.update(main)

        self.log_audit(
            actor_username,
            "UPDATE_CTO",
            main.id,
            old_value=old,
            new_value=data.model_dump(),
            **self._meta(),
        )
        return main

    # ── SHED UPDATE ───────────────────────────────────────────────────
    def update_shed(
        self,
        main_id: int,
        data: ShedUpdate,
        actor_username: str = "system",
    ) -> MainData:
        main = self.get_by_id_or_404(main_id)
        old = {"shed": main.shed}
        main.shed = data.shed
        self.repo.update(main)

        self.log_audit(
            actor_username,
            "UPDATE_SHED",
            main.id,
            old_value=old,
            new_value=data.model_dump(),
            **self._meta(),
        )
        return main

    # ── LOCO UPDATE ───────────────────────────────────────────────────
    def update_loco(
        self,
        main_id: int,
        data: LocoUpdate,
        actor_username: str = "system",
    ) -> MainData:
        main = self.get_by_id_or_404(main_id)
        old = {"loco1": main.loco1, "loco2": main.loco2, "loco3": main.loco3}
        main.loco1 = data.loco1
        main.loco2 = data.loco2
        main.loco3 = data.loco3
        self.repo.update(main)

        self.log_audit(
            actor_username,
            "UPDATE_LOCO",
            main.id,
            old_value=old,
            new_value=data.model_dump(),
            **self._meta(),
        )
        return main

