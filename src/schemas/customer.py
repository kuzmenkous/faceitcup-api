from datetime import datetime

from pydantic import BaseModel, Field

from src.constants.customer import ErrorStatus
from src.schemas.base import IdSchema


class CustomerCreate(BaseModel):
    invite_code: str = Field(..., exclude=True)


class CustomerUpdate(BaseModel):
    original_steam_connected: bool
    second_steam_connected: bool


class SetCustomerErrorStatus(BaseModel):
    error_status: ErrorStatus


class CustomerRead(CustomerUpdate, SetCustomerErrorStatus, IdSchema):
    hub_id: int
    original_steam_connected: bool
    second_steam_connected: bool
    created_at: datetime


class CustomerErrorStatusUpdate(BaseModel):
    hub_id: int
    error_status: ErrorStatus
