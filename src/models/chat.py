from sqlalchemy import ForeignKey, false, func, select
from sqlalchemy.orm import Mapped, deferred, mapped_column, relationship

from src.constants.chat import AuthorType
from src.models.base import BaseModel, Id
from src.models.customer import CustomerModel


class ChatMessageModel(BaseModel):
    __tablename__ = "chat_messages"

    chat_room_id: Mapped[int] = mapped_column(
        ForeignKey("chat_rooms.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    content: Mapped[str]
    author_type: Mapped[AuthorType]

    room: Mapped["ChatRoomModel"] = relationship()

    def __str__(self) -> str:
        return f"Chat Message: {self.id} in Room: {self.chat_room_id}"


class ChatRoomModel(BaseModel):
    __tablename__ = "chat_rooms"

    id: Mapped[Id] = mapped_column()
    is_customer_in_chat: Mapped[bool] = mapped_column(server_default=false())
    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id", ondelete="CASCADE", onupdate="CASCADE")
    )

    customer: Mapped[CustomerModel] = relationship()
    messages_count: Mapped[int] = deferred(
        select(func.count())
        .where(ChatMessageModel.chat_room_id == id)
        .label("messages_count"),
        raiseload=True,
    )

    @property
    def customer_hub_id(self) -> int:
        return self.customer.hub_id

    def __str__(self) -> str:
        return f"Chat Room: {self.id}"
