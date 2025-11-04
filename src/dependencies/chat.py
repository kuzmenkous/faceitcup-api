from fastapi import WebSocketException, status
from pydantic import PositiveInt

from src.dependencies.db import Session
from src.services.chat import ChatRoomService


async def check_chat_room_exists(
    session: Session, chat_room_id: PositiveInt
) -> None:
    if not await ChatRoomService(session).is_chat_room_exists(chat_room_id):
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
