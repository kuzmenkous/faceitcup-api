from datetime import datetime

from pydantic import BaseModel, Field

from src.schemas.base import IdSchema


class CustomerCreate(BaseModel):
    invite_code: str = Field(..., exclude=True)


class CustomerRead(IdSchema):
    hub_id: int
    original_steam_connected: bool
    second_steam_connected: bool
    created_at: datetime
