import re
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class SignOnDataCreate(BaseModel):
    cms_id: int
    crew_id: str = Field(..., min_length=1, max_length=20)
    crew_name: str = Field(..., min_length=2, max_length=100)
    status: str = Field(..., max_length=30)
    train_no: str = Field(..., max_length=20)
    from_station: str = Field(..., max_length=20)
    to_station: str = Field(..., max_length=20)
    sign_on_time: str = Field(..., max_length=30)
    cto_train_no: str = Field(..., max_length=20)
    cto_station: str = Field(..., max_length=20)
    cto_time: str = Field(..., max_length=30)
    loco1: str = Field(..., max_length=20)
    loco2: str = Field("", max_length=20)
    loco3: str = Field("", max_length=20)
    shed: str = Field(..., max_length=30)

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

    @field_validator("from_station", "to_station", "cto_station")
    @classmethod
    def validate_station_code(cls, v: str) -> str:
        if not re.match(r"^[A-Z]{2,4}$", v):
            raise ValueError("Station code must be 2-4 uppercase letters (e.g., NDLS, BCT)")
        return v


class SignOnDataUpdate(BaseModel):
    status: Optional[str] = None
    train_no: Optional[str] = None
    from_station: Optional[str] = None
    to_station: Optional[str] = None
    sign_on_time: Optional[str] = None
    cto_train_no: Optional[str] = None
    cto_station: Optional[str] = None
    cto_time: Optional[str] = None
    loco1: Optional[str] = None
    loco2: Optional[str] = None
    loco3: Optional[str] = None
    shed: Optional[str] = None


class SignOnDataResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    cms_id: int
    crew_id: str
    crew_name: str
    status: str
    train_no: str
    from_station: str
    to_station: str
    sign_on_time: str
    cto_train_no: str
    cto_station: str
    cto_time: str
    loco1: str
    loco2: str
    loco3: str
    shed: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

