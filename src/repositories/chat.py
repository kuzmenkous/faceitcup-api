from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, undefer

from src.models.chat import ChatMessageModel, ChatRoomModel
from src.models.customer import CustomerModel
from src.repositories.base import Repository


class ChatRoomRepository:
    _repository: Repository[ChatRoomModel] = Repository(ChatRoomModel)

    async def get_chat_rooms(
        self, session: AsyncSession
    ) -> tuple[ChatRoomModel, ...]:
        stmt = (
            select(ChatRoomModel)
            .where(CustomerModel.second_steam_connected)
            .options(
                undefer(ChatRoomModel.messages_count),
                joinedload(ChatRoomModel.customer).load_only(
                    CustomerModel.hub_id
                ),
            )
        )
        return tuple((await session.execute(stmt)).scalars())

    async def is_chat_room_exists(
        self, session: AsyncSession, chat_room_id: int
    ) -> bool:
        return await self._repository.exists(
            session, (ChatRoomModel.id == chat_room_id,)
        )

    async def update_chat_room_is_customer_in_chat(
        self,
        session: AsyncSession,
        chat_room_id: int,
        is_customer_in_chat: bool,
    ) -> None:
        stmt = (
            update(ChatRoomModel)
            .where(ChatRoomModel.id == chat_room_id)
            .values(is_customer_in_chat=is_customer_in_chat)
        )
        await session.execute(stmt)


class ChatMessageRepository:
    _repository: Repository[ChatMessageModel] = Repository(ChatMessageModel)

    async def get_messages_by_chat_room_id(
        self, session: AsyncSession, chat_room_id: int
    ) -> tuple[ChatMessageModel, ...]:
        return await self._repository.get_all(
            session, (ChatMessageModel.chat_room_id == chat_room_id,)
        )

    async def get_messages_count_by_chat_room_id(
        self, session: AsyncSession, chat_room_id: int
    ) -> int:
        stmt = select(func.count()).where(
            ChatMessageModel.chat_room_id == chat_room_id
        )
        return (await session.execute(stmt)).scalar_one()
