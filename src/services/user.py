from uuid import UUID

from argon2.exceptions import VerifyMismatchError
from fastapi import HTTPException, status
from sqlalchemy.exc import NoResultFound

from src.constants.user import password_hasher
from src.models.user import SessionModel, UserModel
from src.repositories.user import SessionRepository, UserRepository
from src.schemas.user import UserCredentials
from src.services.base import BaseService


class UserService(BaseService):
    async def get_user_by_credentials(
        self, credentials: UserCredentials
    ) -> UserModel:
        try:
            user = await UserRepository().get_user_by_username(
                self._session, credentials.username
            )
            password_hasher.verify(
                user.hashed_password, credentials.password.get_secret_value()
            )
        except (NoResultFound, VerifyMismatchError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
            )
        if password_hasher.check_needs_rehash(user.hashed_password):
            user.hashed_password = password_hasher.hash(
                credentials.password.get_secret_value()
            )
            self._session.add(user)
            await self._session.commit()
        return user


class SessionService(BaseService):
    async def get_session_by_token(self, token: UUID) -> SessionModel:
        user_session = await SessionRepository().get_session_by_token(
            self._session, token
        )
        if not user_session:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )
        return user_session

    async def delete_session_by_token(self, token: UUID) -> None:
        await SessionRepository().delete_session_by_token(self._session, token)
