from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import BaseModel
from src.models.user import UserIdMixin


class InviteCodeModel(UserIdMixin, BaseModel):
    __tablename__ = "invite_codes"

    code: Mapped[str] = mapped_column(unique=True)

    def __str__(self) -> str:
        return f"InviteCode: {self.code}."
