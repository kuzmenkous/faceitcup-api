from typing import Any

from fastapi import (
    APIRouter,
    Depends,
    WebSocket,
    WebSocketDisconnect,
    WebSocketException,
    status,
)
from pydantic import PositiveInt, ValidationError
from sqlalchemy.exc import NoResultFound

from src.constants.chat import AuthorType, NotificationType
from src.core.db.session import session_getter
from src.dependencies.chat import check_chat_room_exists
from src.models.chat import ChatMessageModel
from src.schemas.chat import ChatMessage, ChatMessageCreate, ChatNotification
from src.services.chat import ChatMessageService, ChatRoomService
from src.ws.managers.chat import (
    chat_connection_manager,
    chat_notification_connection_manager,
)

chat_router = APIRouter(prefix="/chat", tags=["Chat"])


async def _process_and_save_message(
    chat_room_id: PositiveInt,
    author_type: AuthorType,
    message_data: dict[str, Any],
) -> None:
    chat_message_create = ChatMessageCreate(
        author_type=author_type,
        content=message_data["content"],
        chat_room_id=chat_room_id,
    )

    async with session_getter.begin() as session:
        chat_message_model = ChatMessageModel(
            **chat_message_create.model_dump()
        )
        session.add(chat_message_model)
        await session.flush()

        chat_message_to_send = ChatMessage.model_validate(chat_message_model)
        await chat_connection_manager.broadcast(chat_message_to_send)

        chat_room_messages_count = await ChatMessageService(
            session
        ).get_messages_count_by_chat_room_id(chat_room_id)

        await chat_notification_connection_manager.broadcast(
            ChatNotification(
                type=NotificationType.ROOM_MESSAGES_COUNT_UPDATE,
                chat_room_id=chat_room_id,
                room_messages_count=chat_room_messages_count,
            )
        )


async def _send_customer_connection_notification(
    chat_room_id: PositiveInt, connected: bool
) -> None:
    await chat_notification_connection_manager.broadcast(
        ChatNotification(
            type=NotificationType.CUSTOMER_ROOM_CONNECTION_UPDATE,
            chat_room_id=chat_room_id,
            connected=connected,
        )
    )


async def _handle_chat_websocket(
    websocket: WebSocket, chat_room_id: PositiveInt, author_type: AuthorType
) -> None:
    await chat_connection_manager.connect(
        websocket=websocket, chat_room_id=chat_room_id
    )

    if author_type == AuthorType.CUSTOMER:
        async with session_getter.begin() as session:
            await ChatRoomService(
                session
            ).update_chat_room_is_customer_in_chat(chat_room_id, True)

        await _send_customer_connection_notification(
            chat_room_id=chat_room_id, connected=True
        )

    try:
        while True:
            message_data: dict[str, Any] = await websocket.receive_json()
            await _process_and_save_message(
                chat_room_id=chat_room_id,
                author_type=author_type,
                message_data=message_data,
            )
    except NoResultFound:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    except (KeyError, ValidationError):
        raise WebSocketException(code=status.WS_1003_UNSUPPORTED_DATA)
    except WebSocketDisconnect:
        await chat_connection_manager.disconnect(
            websocket=websocket, chat_room_id=chat_room_id
        )
        if author_type == AuthorType.CUSTOMER:
            async with session_getter.begin() as session:
                await ChatRoomService(
                    session
                ).update_chat_room_is_customer_in_chat(chat_room_id, False)

            await _send_customer_connection_notification(
                chat_room_id=chat_room_id, connected=False
            )


@chat_router.websocket(
    "/customer/{chat_room_id}", dependencies=[Depends(check_chat_room_exists)]
)
async def customer_chat(
    websocket: WebSocket, chat_room_id: PositiveInt
) -> None:
    await _handle_chat_websocket(
        websocket=websocket,
        chat_room_id=chat_room_id,
        author_type=AuthorType.CUSTOMER,
    )


@chat_router.websocket(
    "/admin/{chat_room_id}", dependencies=[Depends(check_chat_room_exists)]
)
async def admin_chat(websocket: WebSocket, chat_room_id: PositiveInt) -> None:
    await _handle_chat_websocket(
        websocket=websocket,
        chat_room_id=chat_room_id,
        author_type=AuthorType.ADMIN,
    )


@chat_router.websocket("/notifications")
async def chat_notifications(websocket: WebSocket) -> None:
    await chat_notification_connection_manager.connect(websocket=websocket)

    try:
        while True:
            await websocket.receive_json()
    except WebSocketDisconnect:
        await chat_notification_connection_manager.disconnect(
            websocket=websocket
        )
