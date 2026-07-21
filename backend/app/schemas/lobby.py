from pydantic import BaseModel, ConfigDict


class LobbyCreate(BaseModel):
    name: str
    is_active: bool = True


class LobbyUpdate(BaseModel):
    name: str | None = None
    is_active: bool | None = None


class LobbyResponse(BaseModel):
    id: int
    name: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
