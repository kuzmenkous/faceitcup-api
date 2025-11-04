from src.models.chat import ChatMessageModel, ChatRoomModel
from src.repositories.chat import ChatMessageRepository, ChatRoomRepository
from src.services.base import BaseService


class ChatRoomService(BaseService):
    async def get_chat_rooms(self) -> tuple[ChatRoomModel, ...]:
        return await ChatRoomRepository().get_chat_rooms(self._session)

    async def is_chat_room_exists(self, chat_room_id: int) -> bool:
        return await ChatRoomRepository().is_chat_room_exists(
            self._session, chat_room_id
        )

    async def update_chat_room_is_customer_in_chat(
        self, chat_room_id: int, is_customer_in_chat: bool
    ) -> None:
        await ChatRoomRepository().update_chat_room_is_customer_in_chat(
            self._session, chat_room_id, is_customer_in_chat
        )


class ChatMessageService(BaseService):
    async def get_messages_by_chat_room_id(
        self, chat_room_id: int
    ) -> tuple[ChatMessageModel, ...]:
        return await ChatMessageRepository().get_messages_by_chat_room_id(
            self._session, chat_room_id
        )

    async def get_messages_count_by_chat_room_id(
        self, chat_room_id: int
    ) -> int:
        return (
            await ChatMessageRepository().get_messages_count_by_chat_room_id(
                self._session, chat_room_id
            )
        )
