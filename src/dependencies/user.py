from typing import Annotated
from uuid import UUID

from fastapi import Body, Depends, Response
from fastapi.security.api_key import APIKeyCookie

from src.constants.user import SESSION_TOKEN
from src.dependencies.db import Session
from src.models.user import SessionModel, UserModel
from src.schemas.user import UserCredentials
from src.services.user import SessionService, UserService
from src.utils import set_auth_data_to_response_cookie


async def get_user_by_credentials(
    session: Session, credentials: Annotated[UserCredentials, Body()]
) -> UserModel:
    return await UserService(session).get_user_by_credentials(credentials)


async def get_session_token(
    session_token: Annotated[
        str,
        Depends(
            APIKeyCookie(
                scheme_name=SESSION_TOKEN,
                name=SESSION_TOKEN,
                description="Type: UUID",
            )
        ),
    ],
) -> UUID:
    return UUID(session_token)


SessionToken = Annotated[UUID, Depends(get_session_token)]


async def get_user_session_by_api_token(
    db_session: Session, session_token: SessionToken, response: Response
) -> SessionModel:
    user_session = await SessionService(db_session).get_session_by_token(
        session_token
    )
    set_auth_data_to_response_cookie(response, user_session)
    return user_session


UserSession = Annotated[SessionModel, Depends(get_user_session_by_api_token)]


async def get_user_by_api_token(user_session: UserSession) -> UserModel:
    return user_session.user


LoggedInUser = Annotated[UserModel, Depends(get_user_by_api_token)]
