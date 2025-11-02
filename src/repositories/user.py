from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.models.invite_code import InviteCodeModel
from src.models.user import SessionModel, UserModel
from src.repositories.base import Repository


class UserRepository:
    _repository: Repository[UserModel] = Repository(UserModel)

    async def get_user_by_username(
        self, session: AsyncSession, username: str
    ) -> UserModel:
        return await self._repository.get_one(
            session, (UserModel.username == username,)
        )

    async def get_user_by_invite_code(
        self, session: AsyncSession, invite_code: str
    ) -> UserModel | None:
        stmt = (
            select(UserModel)
            .join(InviteCodeModel)
            .where(InviteCodeModel.code == invite_code)
        )
        return (await session.execute(stmt)).scalar_one_or_none()


class SessionRepository:
    _repository: Repository[SessionModel] = Repository(SessionModel)

    async def get_session_by_token(
        self, session: AsyncSession, token: UUID
    ) -> SessionModel | None:
        stmt = (
            select(SessionModel)
            .where(SessionModel.token == token)
            .options(joinedload(SessionModel.user, innerjoin=True))
        )
        return (await session.execute(stmt)).scalar_one_or_none()

    async def delete_session_by_token(
        self, session: AsyncSession, token: UUID
    ) -> None:
        stmt = delete(SessionModel).where(SessionModel.token == token)
        await session.execute(stmt)
