from fastapi import Response

from src.constants.user import SESSION_TOKEN
from src.models.user import SessionModel


def set_auth_data_to_response_cookie(
    response: Response, user_session: SessionModel
) -> None:
    response.set_cookie(key=SESSION_TOKEN, value=str(user_session.token))
