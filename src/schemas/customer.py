from datetime import datetime
from typing import Self

from pydantic import BaseModel, model_validator

from src.constants.customer import ErrorStatus
from src.schemas.base import IdSchema


class CustomerCreate(BaseModel):
    invite_code: str | None = None
    create_verified: bool | None = None

    @model_validator(mode="after")
    def validate_invite_code(self) -> Self:
        if not self.create_verified and not self.invite_code:
            raise ValueError(
                "Invite code is required for unverified customer creation."
            )
        return self


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
