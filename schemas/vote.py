from pydantic import BaseModel, ConfigDict
from datetime import datetime


class SVote(BaseModel):
    option_index: int


class SVoteCreate(SVote):
    pass


class SVoteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    poll_id: int
    created_at: datetime
    option_index: int