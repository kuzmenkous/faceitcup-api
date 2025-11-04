from typing import Annotated

from fastapi import APIRouter, Depends

from src.adapters.broker import broker
from src.dependencies.customer import get_customer_model
from src.dependencies.db import Session
from src.models.customer import CustomerModel
from src.schemas.customer import (
    CustomerCreate,
    CustomerErrorStatusUpdate,
    CustomerRead,
    CustomerUpdate,
    SetCustomerErrorStatus,
)
from src.services.customer import CustomerService

customers_router = APIRouter(prefix="/customers", tags=["Customers"])


@customers_router.post("", response_description="id of the created customer")
async def create_customer(
    session: Session, customer_create: CustomerCreate
) -> int:
    return await CustomerService(session).create_customer(customer_create)


@customers_router.get("")
async def get_customers(session: Session) -> tuple[CustomerRead, ...]:
    return tuple(
        CustomerRead.model_validate(customer)
        for customer in await CustomerService(session).get_customers()
    )


@customers_router.get("/{customer_id}")
async def get_customer(
    customer_model: Annotated[CustomerModel, Depends(get_customer_model)],
) -> CustomerRead:
    return CustomerRead.model_validate(customer_model)


@customers_router.put("/{customer_id}")
async def update_customer(
    customer_model: Annotated[CustomerModel, Depends(get_customer_model)],
    customer_update: CustomerUpdate,
) -> None:
    for field_name, value in customer_update.model_dump().items():
        setattr(customer_model, field_name, value)


@customers_router.post("/{customer_id}/set_error")
async def set_customer_error_status(
    customer_model: Annotated[CustomerModel, Depends(get_customer_model)],
    error_status_data: SetCustomerErrorStatus,
) -> None:
    customer_model.error_status = error_status_data.error_status

    await broker.publish(
        CustomerErrorStatusUpdate(
            hub_id=customer_model.hub_id,
            error_status=error_status_data.error_status,
        ),
        queue="customer_error_status_updates",
    )
