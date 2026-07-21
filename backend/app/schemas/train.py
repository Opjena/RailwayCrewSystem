from pydantic import BaseModel, ConfigDict


class TrainCreate(BaseModel):
    train_number: str
    is_active: bool = True


class TrainUpdate(BaseModel):
    train_number: str | None = None
    is_active: bool | None = None


class TrainResponse(BaseModel):
    id: int
    train_number: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
