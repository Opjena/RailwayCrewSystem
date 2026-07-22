import re
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class MainDataResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    signon_id: int
    crew_id: str
    crew_name: str
    train_no: str
    from_station: str
    to_station: str
    status: str
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


class CTOUpdate(BaseModel):
    cto_train_no: str = Field(..., max_length=20)
    cto_station: str = Field(..., max_length=20)
    cto_time: str = Field(..., max_length=30)

    @field_validator("cto_station")
    @classmethod
    def validate_station_code(cls, v: str) -> str:
        if not re.match(r"^[A-Z]{2,4}$", v):
            raise ValueError("Station code must be 2-4 uppercase letters (e.g., NDLS, BCT)")
        return v

    @field_validator("cto_train_no")
    @classmethod
    def validate_train_no(cls, v: str) -> str:
        if not re.match(r"^\d{4,6}$", v):
            raise ValueError("Train number must be 4-6 digits")
        return v


class ShedUpdate(BaseModel):
    shed: str = Field(..., min_length=1, max_length=30)


class LocoUpdate(BaseModel):
    loco1: str = Field(..., max_length=20)
    loco2: str = Field("", max_length=20)
    loco3: str = Field("", max_length=20)

