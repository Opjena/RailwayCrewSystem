from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog


class AuditLogService:
    @staticmethod
    def log_action(
        db: Session,
        actor_username: str | None,
        action: str,
        entity: str,
        entity_id: str | None = None,
    ) -> AuditLog:
        log = AuditLog(
            actor_username=actor_username,
            action=action,
            entity=entity,
            entity_id=entity_id,
        )
        db.add(log)
        db.commit()
        db.refresh(log)
        return log
