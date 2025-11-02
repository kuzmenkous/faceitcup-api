from typing import Annotated

from pydantic import Field
from pydantic_settings import BaseSettings
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncSession

from src.models.user import UserModel
from src.schemas.user import UserCreate, _PasswordForCheck


class SuperadminCredentials(UserCreate, BaseSettings):
    username: Annotated[str, Field(validation_alias="SUPERADMIN_USERNAME")]
    password: Annotated[
        _PasswordForCheck, Field(validation_alias="SUPERADMIN_PASSWORD")
    ]
    password2: Annotated[
        _PasswordForCheck, Field(validation_alias="SUPERADMIN_PASSWORD")
    ]


superadmin_credentials = SuperadminCredentials()


async def insert_first_rows_with_async_connection(
    async_connection: AsyncConnection,
) -> None:
    session = AsyncSession(async_connection)
    await create_first_rows(session)
    await session.flush()


async def create_first_rows(session: AsyncSession) -> None:
    # Create superuser
    user = UserModel(
        username=superadmin_credentials.username,
        hashed_password=superadmin_credentials.hashed_password,
    )
    session.add(user)
