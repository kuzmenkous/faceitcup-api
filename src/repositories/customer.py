from sqlalchemy import exists
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.customer import CustomerModel
from src.repositories.base import Repository


class CustomerRepository:
    _repository: Repository[CustomerModel] = Repository(CustomerModel)

    async def get_customers(
        self, session: AsyncSession
    ) -> tuple[CustomerModel, ...]:
        return await self._repository.get_all(
            session, (CustomerModel.second_steam_connected.is_(True),)
        )

    async def get_customer(
        self, session: AsyncSession, customer_id: int
    ) -> CustomerModel:
        return await session.get_one(CustomerModel, customer_id)

    async def check_exists_by_hub_id(
        self, session: AsyncSession, hub_id: int
    ) -> bool:
        return (
            await session.execute(
                exists().where(CustomerModel.hub_id == hub_id).select()
            )
        ).scalar_one()
