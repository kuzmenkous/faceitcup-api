from pydantic import PositiveInt

from src.dependencies.db import Session
from src.models.customer import CustomerModel
from src.services.customer import CustomerService


async def get_customer_model(
    session: Session, customer_id: PositiveInt
) -> CustomerModel:
    return await CustomerService(session).get_customer(customer_id)
