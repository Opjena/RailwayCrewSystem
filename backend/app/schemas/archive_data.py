from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ArchiveDataResponse(BaseModel):
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
    archived_at: datetime

