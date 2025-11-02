from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.invite_code import InviteCodeModel
from src.repositories.base import Repository


class InviteCodeRepository:
    _repository: Repository[InviteCodeModel] = Repository(InviteCodeModel)

    async def get_invite_code_by_id(
        self, session: AsyncSession, invite_code_id: int
    ) -> InviteCodeModel:
        return await self._repository.get_one(
            session, (InviteCodeModel.id == invite_code_id,)
        )

    async def get_invite_code_by_code(
        self, session: AsyncSession, code: str
    ) -> InviteCodeModel | None:
        stmt = select(InviteCodeModel).where(InviteCodeModel.code == code)
        return (await session.execute(stmt)).scalar_one_or_none()

    async def get_all_invite_codes(
        self, session: AsyncSession
    ) -> tuple[InviteCodeModel, ...]:
        stmt = select(InviteCodeModel)
        return tuple(await session.scalars(stmt))

    async def delete_invite_code_by_id(
        self, session: AsyncSession, invite_code_id: int
    ) -> None:
        stmt = delete(InviteCodeModel).where(
            InviteCodeModel.id == invite_code_id
        )
        await session.execute(stmt)
