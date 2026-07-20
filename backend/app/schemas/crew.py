from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from app.core.enums import Department


class CrewCreate(BaseModel):
    crew_id: str
    full_name: str
    department: Department
    email: EmailStr
    phone: str | None = None


class CrewUpdate(BaseModel):
    full_name: str | None = None
    department: Department | None = None
    email: EmailStr | None = None
    phone: str | None = None
    is_active: bool | None = None


class CrewResponse(BaseModel):
    id: int
    crew_id: str
    full_name: str
    department: Department
    email: EmailStr
    phone: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CrewListResponse(BaseModel):
    id: int
    crew_id: str
    full_name: str
    department: Department
    email: EmailStr
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
