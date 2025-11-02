from src.models.user import UserModel
from src.repositories.base import Repository


class UserRepository:
    _repository: Repository[UserModel]
