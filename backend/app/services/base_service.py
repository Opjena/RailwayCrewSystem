"""
BaseService — Common CRUD orchestration for all modules.

Every service should inherit from this to get standard:
  - CRUD helpers that delegate to the repository layer
  - Audit-logging helper
  - Common error handling
  - Pagination helpers
"""

import json
from datetime import datetime
from typing import Any, Generic, Optional, TypeVar

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog
from app.repositories.base_repository import BaseRepository

ModelType = TypeVar("ModelType")


class BaseService(Generic[ModelType]):
    """
    Generic service providing standard business-logic helpers.

    Subclasses set:
        self.repo = SomeRepository(db)
        self.model_class = SomeModel
        self.entity_name = "SomeEntity"
    """

    def __init__(self, db: Session):
        self.db = db
        self.repo: Optional[BaseRepository] = None
        self.model_class: type | None = None
        self.entity_name: str = "Record"

    # ------------------------------------------------------------------
    # Audit Logging
    # ------------------------------------------------------------------
    def log_audit(
        self,
        actor_username: str,
        action: str,
        entity_id: str | int | None = None,
        old_value: dict[str, Any] | None = None,
        new_value: dict[str, Any] | None = None,
        ip_address: str | None = None,
        user_agent: str | None = None,
    ) -> None:
        """Insert an audit-log row."""
        log = AuditLog(
            actor_username=actor_username,
            action=action,
            entity=self.entity_name,
            entity_id=str(entity_id) if entity_id is not None else None,
            old_value=json.dumps(old_value) if old_value is not None else None,
            new_value=json.dumps(new_value) if new_value is not None else None,
            ip_address=ip_address,
            user_agent=user_agent,
            created_at=datetime.utcnow(),
        )
        self.db.add(log)
        self.db.flush()

    # ------------------------------------------------------------------
    # Common CRUD (thin wrappers)
    # ------------------------------------------------------------------
    def get_by_id_or_404(self, id: int) -> ModelType:
        """Return record or raise 404."""
        record = self.repo.get_by_id(id) if self.repo else None
        if not record:
            raise HTTPException(
                status_code=404,
                detail=f"{self.entity_name} not found",
            )
        return record

    def create_record(
        self,
        actor_username: str,
        **data: Any,
    ) -> ModelType:
        """Create, audit-log, return."""
        if not self.repo:
            raise NotImplementedError("repo not set")
        instance = self.repo.create(**data)
        self.log_audit(actor_username, "CREATE", getattr(instance, "id", None))
        return instance

    def update_record(
        self,
        id: int,
        actor_username: str,
        **data: Any,
    ) -> ModelType:
        """Fetch, apply updates, audit-log, return."""
        instance = self.get_by_id_or_404(id)
        old = {k: getattr(instance, k) for k in data if hasattr(instance, k)}
        if self.repo:
            instance = self.repo.update(instance, **data)
        self.log_audit(
            actor_username,
            "UPDATE",
            id,
            old_value=old if old else None,
            new_value=data,
        )
        return instance

    def soft_delete_record(
        self,
        id: int,
        actor_username: str,
    ) -> dict[str, Any]:
        """Soft-delete (deactivate) a record."""
        instance = self.get_by_id_or_404(id)
        if self.repo:
            self.repo.soft_delete(instance)
        self.log_audit(actor_username, "DEACTIVATE", id)
        return {"message": f"{self.entity_name} deactivated successfully"}

    # ------------------------------------------------------------------
    # Pagination helper
    # ------------------------------------------------------------------
    def paginated_response(
        self,
        items: list,
        total: int,
        page: int,
        page_size: int,
    ) -> dict:
        """Build a standard paginated response dict."""
        return {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size if page_size else 0,
        }


