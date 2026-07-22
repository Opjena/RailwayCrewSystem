import re
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.enums import Department


class CrewCreate(BaseModel):
    crew_id: str = Field(..., min_length=1, max_length=50)
    full_name: str = Field(..., min_length=2, max_length=100)
    department: Department
    mobile_number: str = Field(..., min_length=10, max_length=15)
    designation: str = Field(..., min_length=2, max_length=50)
    password: str = Field(..., min_length=8)

    @field_validator("crew_id")
    @classmethod
    def validate_crew_id(cls, v: str) -> str:
        if not re.match(r"^CR\d{3,5}$", v):
            raise ValueError(
                "Crew ID must match pattern CR followed by 3-5 digits (e.g., CR001, CR00123)"
            )
        return v

    @field_validator("mobile_number")
    @classmethod
    def validate_mobile(cls, v: str) -> str:
        # Accept 10-digit mobile numbers, optionally with +91 or 0 prefix
        cleaned = v.replace(" ", "").replace("-", "")
        if cleaned.startswith("+91"):
            cleaned = cleaned[3:]
        elif cleaned.startswith("0"):
            cleaned = cleaned[1:]
        if not cleaned.isdigit() or len(cleaned) != 10:
            raise ValueError("Mobile number must be a valid 10-digit Indian mobile number")
        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[0-9]", v):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>_\-]", v):
            raise ValueError("Password must contain at least one special character")
        return v


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

