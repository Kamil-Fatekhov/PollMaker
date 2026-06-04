from pydantic import BaseModel, ConfigDict
from datetime import datetime


class SPoll(BaseModel):
    title: str
    description: str | None = None


class SPollCreate(SPoll):
    options: list[str]


class SPollUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    is_closed: bool | None = None


class SPollResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    description: str
    options: list[str]
    creator_id: int
    created_at: datetime
    is_closed: bool
