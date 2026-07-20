from pydantic import BaseModel, ConfigDict
from datetime import datetime, date, time
from app.core.enums import ShiftType


class ShiftCreate(BaseModel):
    shift_date: date
    shift_type: ShiftType
    start_time: time
    end_time: time
    crew_required: int = 1
    location: str | None = None
    notes: str | None = None


class ShiftUpdate(BaseModel):
    shift_type: ShiftType | None = None
    start_time: time | None = None
    end_time: time | None = None
    crew_required: int | None = None
    location: str | None = None
    notes: str | None = None


class ShiftResponse(BaseModel):
    id: int
    shift_date: date
    shift_type: ShiftType
    start_time: time
    end_time: time
    crew_required: int
    location: str | None
    notes: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ShiftListResponse(BaseModel):
    id: int
    shift_date: date
    shift_type: ShiftType
    start_time: time
    end_time: time
    crew_required: int
    location: str | None

    model_config = ConfigDict(from_attributes=True)
