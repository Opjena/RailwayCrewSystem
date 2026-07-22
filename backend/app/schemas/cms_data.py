import re
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class CMSDataCreate(BaseModel):
    crew_id: str = Field(..., min_length=1, max_length=20)
    crew_name: str = Field(..., min_length=2, max_length=100)
    crew_designation: str = Field(..., min_length=2, max_length=50)

    fortnight_hours: str = Field(..., max_length=20)

    avail_time: str = Field(..., max_length=30)
    avail_station: str = Field(..., max_length=50)

    status: str = Field(..., max_length=30)

    called_time: str = Field(..., max_length=30)
    ack_time: str = Field(..., max_length=30)
    sign_on_time: str = Field(..., max_length=30)
    last_signoff_time: str = Field(..., max_length=30)

    train_no: str = Field(..., max_length=20)
    from_station: str = Field(..., max_length=20)
    to_station: str = Field(..., max_length=20)

    @field_validator("crew_id")
    @classmethod
    def validate_crew_id(cls, v: str) -> str:
        if not re.match(r"^CR\d{3,5}$", v):
            raise ValueError(
                "Crew ID must match pattern CR followed by 3-5 digits (e.g., CR001)"
            )
        return v

    @field_validator("train_no")
    @classmethod
    def validate_train_no(cls, v: str) -> str:
        if not re.match(r"^\d{4,6}$", v):
            raise ValueError("Train number must be 4-6 digits")
        return v

    @field_validator("from_station", "to_station")
    @classmethod
    def validate_station_code(cls, v: str) -> str:
        if not re.match(r"^[A-Z]{2,4}$", v):
            raise ValueError("Station code must be 2-4 uppercase letters (e.g., NDLS, BCT)")
        return v


class CMSDataUpdate(BaseModel):
    crew_name: Optional[str] = None
    crew_designation: Optional[str] = None
    fortnight_hours: Optional[str] = None
    avail_time: Optional[str] = None
    avail_station: Optional[str] = None
    status: Optional[str] = None
    called_time: Optional[str] = None
    ack_time: Optional[str] = None
    sign_on_time: Optional[str] = None
    last_signoff_time: Optional[str] = None
    train_no: Optional[str] = None
    from_station: Optional[str] = None
    to_station: Optional[str] = None
    is_active: Optional[bool] = None


class CMSDataResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    crew_id: str
    crew_name: str
    crew_designation: str
    fortnight_hours: str
    avail_time: str
    avail_station: str
    status: str
    called_time: str
    ack_time: str
    sign_on_time: str
    last_signoff_time: str
    train_no: str
    from_station: str
    to_station: str
    is_active: bool
    is_imported: bool
    created_at: datetime
    updated_at: datetime

