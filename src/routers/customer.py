from fastapi import APIRouter

from src.dependencies.db import Session
from src.schemas.customer import CustomerCreate, CustomerRead
from src.services.customer import CustomerService

customers_router = APIRouter(prefix="/customers", tags=["Customers"])


@customers_router.post("", response_description="id of the created customer")
async def create_customer(
    db_session: Session, customer_create: CustomerCreate
) -> int:
    return await CustomerService(db_session).create_customer(customer_create)


@customers_router.get("")
async def get_customers(db_session: Session) -> tuple[CustomerRead, ...]:
    return tuple(
        CustomerRead.model_validate(customer)
        for customer in await CustomerService(db_session).get_customers()
    )


@customers_router.get("/{customer_id}")
async def get_customer(db_session: Session, customer_id: int) -> CustomerRead:
    return CustomerRead.model_validate(
        await CustomerService(db_session).get_customer(customer_id)
    )
