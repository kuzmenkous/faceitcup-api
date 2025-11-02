from src.models.invite_code import InviteCodeModel
from src.repositories.invite_code import InviteCodeRepository
from src.schemas.invite_code import InviteCodeCreate
from src.services.base import BaseService


class InviteCodeService(BaseService):
    async def create_invite_code(
        self, invite_code_data: InviteCodeCreate, user_id: int
    ) -> int:
        invite_code = InviteCodeModel(
            code=invite_code_data.code, user_id=user_id
        )
        self._session.add(invite_code)
        await self._session.flush()
        return invite_code.id

    async def get_all_invite_codes(self) -> tuple[InviteCodeModel, ...]:
        return await InviteCodeRepository().get_all_invite_codes(self._session)

    async def delete_invite_code_by_id(self, invite_code_id: int) -> None:
        await InviteCodeRepository().delete_invite_code_by_id(
            self._session, invite_code_id
        )
