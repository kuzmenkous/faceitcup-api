from fastapi import APIRouter

from src.dependencies.db import Session
from src.schemas.user import UserCreate

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/create", response_description="Id of the created user")
async def create_user(_session: Session, _user_create: UserCreate) -> None:
    return None
