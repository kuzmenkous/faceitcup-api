from functools import cached_property
from typing import Annotated, Self

from pydantic import (
    BaseModel,
    Field,
    SecretStr,
    computed_field,
    model_validator,
)

from src.constants.user import password_hasher
from src.schemas.base import CreatedAtMixin, IdSchema

Password = Annotated[SecretStr, Field(min_length=6)]
_PasswordForCheck = Annotated[Password, Field(exclude=True)]


class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=50)


class UserCreate(UserBase):
    password: _PasswordForCheck
    password2: _PasswordForCheck

    @model_validator(mode="after")
    def check_passwords_match(self) -> Self:
        if (
            self.password.get_secret_value()
            != self.password2.get_secret_value()
        ):
            raise ValueError("Passwords don't match")
        return self

    @computed_field  # type: ignore[prop-decorator]
    @cached_property
    def hashed_password(self) -> str:
        return password_hasher.hash(self.password.get_secret_value())


class UserRead(IdSchema, UserBase, CreatedAtMixin):
    pass


class UserCredentials(BaseModel):
    username: str
    password: _PasswordForCheck
