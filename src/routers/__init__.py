from src.routers.auth import auth_router as auth_router
from src.routers.chat import chat_router as chat_router
from src.routers.customer import customers_router as customers_router
from src.routers.invite_code import invite_codes_router as invite_codes_router

__all__ = [
    "auth_router",
    "chat_router",
    "customers_router",
    "invite_codes_router",
]
