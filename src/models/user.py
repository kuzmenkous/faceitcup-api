from typing import Annotated
from uuid import UUID

from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import BaseModel


class UserModel(BaseModel):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]

    def __str__(self) -> str:
        return f"User: {self.id}"


UserId = Annotated[
    int, ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE")
]


class UserIdMixin:
    user_id: Mapped[UserId]


class SessionModel(UserIdMixin, BaseModel):
    __tablename__ = "sessions"

    token: Mapped[UUID] = mapped_column(
        unique=True, server_default=text("gen_random_uuid()")
    )

    user: Mapped[UserModel] = relationship()

    def __str__(self) -> str:
        return f"Session: {self.id} for User: {self.user_id}"
