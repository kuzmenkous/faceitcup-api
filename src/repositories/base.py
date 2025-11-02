from collections.abc import Iterable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.elements import ColumnElement


class Repository[T]:
    def __init__(self, model: type[T]) -> None:
        self.model = model

    async def get_one(
        self, session: AsyncSession, conditions: Iterable[ColumnElement[bool]]
    ) -> T:
        stmt = select(self.model).where(*conditions)
        return (await session.execute(stmt)).scalar_one()
