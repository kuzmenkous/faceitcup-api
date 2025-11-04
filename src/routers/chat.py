from fastapi import APIRouter

from src.dependencies.db import Session
from src.schemas.chat import ChatMessage, ChatRoomRead
from src.services.chat import ChatMessageService, ChatRoomService

chat_router = APIRouter(prefix="/chat", tags=["Chat"])


@chat_router.get("/rooms")
async def get_chat_rooms(db_session: Session) -> tuple[ChatRoomRead, ...]:
    return tuple(
        ChatRoomRead.model_validate(chat_room)
        for chat_room in await ChatRoomService(db_session).get_chat_rooms()
    )


@chat_router.get("/messages/{chat_room_id}")
async def get_chat_room_messages(
    db_session: Session, chat_room_id: int
) -> tuple[ChatMessage, ...]:
    return tuple(
        ChatMessage.model_validate(message)
        for message in await ChatMessageService(
            db_session
        ).get_messages_by_chat_room_id(chat_room_id)
    )
