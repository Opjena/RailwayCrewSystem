from typing import Any, Optional

from fastapi import HTTPException, Request
from sqlalchemy.orm import Session

from app.auth.hashing import hash_password
from app.models.crew import Crew
from app.repositories.crew_repository import CrewRepository
from app.schemas.crew import CrewCreate, CrewUpdate
from app.services.base_service import BaseService


class CrewService(BaseService[Crew]):
    """Service for Crew module — inherits common CRUD from BaseService."""

    def __init__(self, db: Session, request: Optional[Request] = None):
        super().__init__(db)
        self.repo = CrewRepository(db)
        self.model_class = Crew
        self.entity_name = "Crew"
        self.request = request

    # ── helper to extract request metadata ────────────────────────────
    def _meta(self) -> dict[str, Any]:
        ip = user_agent = None
        if self.request:
            ip = self.request.client.host if self.request.client else None
            user_agent = self.request.headers.get("user-agent")
        return {"ip_address": ip, "user_agent": user_agent}

    # ── CREATE ────────────────────────────────────────────────────────
    def create_crew(self, data: CrewCreate, actor_username: str = "system") -> Crew:
        # Duplicate checks
        if self.repo.get_by_crew_id(data.crew_id):
            raise HTTPException(status_code=400, detail="Crew ID already exists")
        if self.repo.get_by_mobile_number(data.mobile_number):
            raise HTTPException(
                status_code=400, detail="Mobile number already exists"
            )

        crew = self.repo.create(
            crew_id=data.crew_id,
            full_name=data.full_name,
            department=data.department,
            mobile_number=data.mobile_number,
            designation=data.designation,
            password_hash=hash_password(data.password),
            is_active=True,
        )

        self.log_audit(
            actor_username,
            "CREATE",
            crew.crew_id,
            new_value={"crew_id": crew.crew_id, "full_name": crew.full_name},
            **self._meta(),
        )
        return crew

    # ── READ ──────────────────────────────────────────────────────────
    def get_crew_by_crew_id(self, crew_id: str) -> Crew:
        crew = self.repo.get_by_crew_id(crew_id)
        if not crew:
            raise HTTPException(status_code=404, detail="Crew not found")
        return crew

    def get_all_crew(
        self,
        skip: int = 0,
        limit: int = 100,
        department: Optional[str] = None,
        is_active: Optional[bool] = None,
    ):
        filters: dict[str, Any] = {}
        if department is not None:
            filters["department"] = department
        if is_active is not None:
            filters["is_active"] = is_active

        items = self.repo.get_all(skip=skip, limit=limit, filters=filters)
        total = self.repo.count(filters=filters)
        page = (skip // limit) + 1 if limit else 1
        return self.paginated_response(items, total, page, limit)

    # ── UPDATE ────────────────────────────────────────────────────────
    def update_crew(
        self,
        crew_id: str,
        data: CrewUpdate,
        actor_username: str = "system",
    ) -> Crew:
        crew = self.get_crew_by_crew_id(crew_id)

        # Mobile number duplicate check
        if data.mobile_number and data.mobile_number != crew.mobile_number:
            if self.repo.get_by_mobile_number(data.mobile_number):
                raise HTTPException(
                    status_code=400, detail="Mobile number already exists"
                )

        update_data = data.model_dump(exclude_unset=True)
        old = {k: getattr(crew, k) for k in update_data}

        for key, value in update_data.items():
            setattr(crew, key, value)
        self.repo.update(crew)

        self.log_audit(
            actor_username,
            "UPDATE",
            crew.crew_id,
            old_value=old,
            new_value=update_data,
            **self._meta(),
        )
        return crew

    # ── SOFT DELETE ───────────────────────────────────────────────────
    def delete_crew(self, crew_id: str, actor_username: str = "system") -> dict:
        crew = self.get_crew_by_crew_id(crew_id)
        self.repo.soft_delete(crew)

        self.log_audit(
            actor_username,
            "DEACTIVATE",
            crew.crew_id,
            old_value={"is_active": True},
            new_value={"is_active": False},
            **self._meta(),
        )
        return {"message": "Crew deactivated successfully"}

