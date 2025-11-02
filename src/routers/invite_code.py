from fastapi import APIRouter, Depends, status

from src.dependencies.db import Session
from src.dependencies.user import LoggedInUser, get_user_by_api_token
from src.schemas.invite_code import InviteCodeCreate, InviteCodeRead
from src.services.invite_code import InviteCodeService

invite_codes_router = APIRouter(prefix="/invite_codes", tags=["Invite Codes"])


@invite_codes_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_description="id of the created invite code",
)
async def create_invite_code(
    db_session: Session,
    logged_in_user: LoggedInUser,
    invite_code_create: InviteCodeCreate,
) -> int:
    return await InviteCodeService(db_session).create_invite_code(
        invite_code_create, logged_in_user.id
    )


@invite_codes_router.get("", dependencies=[Depends(get_user_by_api_token)])
async def get_invite_codes(db_session: Session) -> tuple[InviteCodeRead, ...]:
    return tuple(
        InviteCodeRead.model_validate(code)
        for code in await InviteCodeService(db_session).get_all_invite_codes()
    )


@invite_codes_router.delete(
    "/{invite_code_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_user_by_api_token)],
)
async def delete_invite_code(db_session: Session, invite_code_id: int) -> None:
    await InviteCodeService(db_session).delete_invite_code_by_id(
        invite_code_id
    )
