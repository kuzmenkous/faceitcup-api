from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import BaseModel


class UserModel(BaseModel):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]

    def __str__(self) -> str:
        return f"User: {self.id}"
