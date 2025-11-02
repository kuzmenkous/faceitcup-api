from sqlalchemy import false
from sqlalchemy.orm import Mapped, mapped_column

from src.constants.customer import ErrorStatus
from src.models.base import BaseModel
from src.models.user import UserIdMixin


class CustomerModel(UserIdMixin, BaseModel):
    __tablename__ = "customers"

    hub_id: Mapped[int] = mapped_column(unique=True)
    original_steam_connected: Mapped[bool] = mapped_column(
        server_default=false()
    )
    second_steam_connected: Mapped[bool] = mapped_column(
        server_default=false()
    )
    error_status: Mapped[ErrorStatus] = mapped_column(
        server_default=ErrorStatus.CHECKING.name
    )

    def __str__(self) -> str:
        return f"Customer: {self.hub_id}"
