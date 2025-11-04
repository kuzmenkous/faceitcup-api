from datetime import datetime
from typing import Annotated, Literal

from pydantic import BaseModel, Field, NonNegativeInt, PositiveInt, RootModel

from src.constants.chat import AuthorType, NotificationType
from src.core.schemas.base import IdSchema


class ChatRoomRead(IdSchema):
    customer_id: PositiveInt
    customer_hub_id: PositiveInt
    is_customer_in_chat: bool
    messages_count: NonNegativeInt
    created_at: datetime


class ChatMessageCreate(BaseModel):
    author_type: AuthorType
    content: str
    chat_room_id: PositiveInt


class ChatMessage(ChatMessageCreate, IdSchema):
    created_at: datetime


class ChatNotificationBase[T](BaseModel):
    type: Annotated[T, Field(description="Doesn't change!")]
    chat_room_id: PositiveInt


class CustomerRoomConnectionNotification(
    ChatNotificationBase[
        Literal[NotificationType.CUSTOMER_ROOM_CONNECTION_UPDATE]
    ]
):
    connected: bool


class RoomMessagesCountUpdateNotification(
    ChatNotificationBase[Literal[NotificationType.ROOM_MESSAGES_COUNT_UPDATE]]
):
    room_messages_count: NonNegativeInt


ChatNotification = RootModel[
    Annotated[
        CustomerRoomConnectionNotification
        | RoomMessagesCountUpdateNotification,
        Field(discriminator="type"),
    ]
]
