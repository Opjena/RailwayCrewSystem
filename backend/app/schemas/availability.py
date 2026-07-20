from pydantic import BaseModel, ConfigDict
from datetime import datetime, date
from app.core.enums import AvailabilityStatus


class AvailabilityCreate(BaseModel):
    crew_id: int
    available_date: date
    status: AvailabilityStatus
    reason: str | None = None


class AvailabilityUpdate(BaseModel):
    status: AvailabilityStatus | None = None
    reason: str | None = None


class AvailabilityResponse(BaseModel):
    id: int
    crew_id: int
    available_date: date
    status: AvailabilityStatus
    reason: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
