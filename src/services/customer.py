from fastapi import HTTPException, status

from src.models.chat import ChatRoomModel
from src.models.customer import CustomerModel
from src.repositories.customer import CustomerRepository
from src.repositories.user import UserRepository
from src.schemas.customer import CustomerCreate
from src.services.base import BaseService
from src.utils import generate_8_digit_hub_id


class CustomerService(BaseService):
    async def _generate_unique_hub_id(self) -> int:
        hub_id = generate_8_digit_hub_id()
        while await CustomerRepository().check_exists_by_hub_id(
            self._session, hub_id
        ):
            hub_id = generate_8_digit_hub_id()
        return hub_id

    async def create_customer(self, customer_create: CustomerCreate) -> int:
        customer_create_dict = customer_create.model_dump()

        if customer_create.create_verified:
            user_model = await UserRepository().get_first_user(self._session)
            if not user_model:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No users found to associate with "
                    "the verified customer",
                )
            customer_create_dict.update(
                {
                    "original_steam_connected": True,
                    "second_steam_connected": True,
                }
            )
        else:
            user_model = await UserRepository().get_user_by_invite_code(
                self._session,
                customer_create.invite_code,  # type: ignore[arg-type]
            )
            if not user_model:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Invite code not found",
                )

        customer_model = CustomerModel(
            user_id=user_model.id,
            hub_id=await self._generate_unique_hub_id(),
            **customer_create_dict,
        )
        self._session.add(customer_model)
        await self._session.flush()

        chat_room_model = ChatRoomModel(customer_id=customer_model.id)
        self._session.add(chat_room_model)

        return customer_model.id

    async def get_customers(self) -> tuple[CustomerModel, ...]:
        return await CustomerRepository().get_customers(self._session)

    async def get_customer(self, customer_id: int) -> CustomerModel:
        return await CustomerRepository().get_customer(
            self._session, customer_id
        )
