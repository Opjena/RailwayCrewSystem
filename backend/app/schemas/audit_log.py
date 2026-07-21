from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AuditLogResponse(BaseModel):
    id: int
    actor_username: str | None
    action: str
    entity: str
    entity_id: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
