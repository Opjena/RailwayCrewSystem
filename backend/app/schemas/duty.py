from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DutyCreate(BaseModel):
    duty_code: str
    description: str | None = None
    is_active: bool = True


class DutyUpdate(BaseModel):
    duty_code: str | None = None
    description: str | None = None
    is_active: bool | None = None


class DutyResponse(BaseModel):
    id: int
    duty_code: str
    description: str | None
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
