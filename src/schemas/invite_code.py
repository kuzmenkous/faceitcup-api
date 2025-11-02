from datetime import datetime

from pydantic import BaseModel, Field

from src.schemas.base import IdSchema


class InviteCodeBase(BaseModel):
    code: str = Field(min_length=1, max_length=100)


class InviteCodeCreate(InviteCodeBase):
    pass


class InviteCodeRead(InviteCodeBase, IdSchema):
    created_at: datetime
