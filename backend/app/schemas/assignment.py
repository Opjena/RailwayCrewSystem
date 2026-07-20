from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.core.enums import AssignmentStatus


class AssignmentCreate(BaseModel):
    shift_id: int
    crew_id: int
    status: AssignmentStatus = AssignmentStatus.ASSIGNED


class AssignmentUpdate(BaseModel):
    status: AssignmentStatus | None = None


class AssignmentResponse(BaseModel):
    id: int
    shift_id: int
    crew_id: int
    status: AssignmentStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AssignmentDetailResponse(BaseModel):
    id: int
    shift_id: int
    crew_id: int
    status: AssignmentStatus
    shift: dict
    crew: dict
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
