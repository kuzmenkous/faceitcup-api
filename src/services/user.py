from src.schemas.user import UserCreate
from src.services.base import BaseService


class UserService(BaseService):
    async def create_user(self, _user_create: UserCreate) -> None:
        return None
