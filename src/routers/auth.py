from typing import Annotated

from fastapi import APIRouter, Depends, Response

from src.dependencies.db import Session
from src.dependencies.user import SessionToken, get_user_by_credentials
from src.models.user import SessionModel, UserModel
from src.schemas.user import Login
from src.services.user import SessionService
from src.utils import set_auth_data_to_response_cookie

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/login")
async def log_in(
    db_session: Session,
    user: Annotated[UserModel, Depends(get_user_by_credentials)],
    response: Response,
) -> Login:
    user_session = SessionModel(user_id=user.id)
    db_session.add(user_session)
    await db_session.flush()
    set_auth_data_to_response_cookie(response, user_session)
    return Login(user=user)


@auth_router.post("/logout")
async def log_out(db_session: Session, session_token: SessionToken) -> None:
    await SessionService(db_session).delete_session_by_token(session_token)
