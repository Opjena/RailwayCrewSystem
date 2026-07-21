from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.core.enums import Department


class CrewCreate(BaseModel):
    crew_id: str = Field(..., min_length=1, max_length=50)
    full_name: str = Field(..., min_length=2, max_length=100)
    department: Department
    mobile_number: str = Field(..., min_length=10, max_length=15)
    designation: str = Field(..., min_length=2, max_length=50)
    password: str = Field(..., min_length=8)


class CrewUpdate(BaseModel):
    full_name: Optional[str] = None
    department: Optional[Department] = None
    mobile_number: Optional[str] = None
    designation: Optional[str] = None
    is_active: Optional[bool] = None


class CrewResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    crew_id: str
    full_name: str
    department: Department
    mobile_number: str
    designation: str
    is_active: bool
    created_at: datetime
    updated_at: datetime


class CrewListResponse(BaseModel):
    total: int
    items: list[CrewResponse]

