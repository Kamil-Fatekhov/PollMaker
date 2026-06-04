from pydantic import BaseModel, ConfigDict
from datetime import datetime


class SUser(BaseModel):
    username: str
    password: str


class SUserCreate(SUser):
    pass


class SUserLogin(SUser):
    pass


class SUserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    username: str