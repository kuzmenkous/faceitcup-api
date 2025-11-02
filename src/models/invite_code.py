from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import BaseModel
from src.models.user import UserIdMixin, UserModel


class InviteCodeModel(UserIdMixin, BaseModel):
    __tablename__ = "invite_codes"

    code: Mapped[str] = mapped_column(unique=True)

    user: Mapped[UserModel] = relationship()

    def __str__(self) -> str:
        return f"InviteCode: {self.code}."
