from fastapi import FastAPI

from src.core.config import settings
from src.ws.routers import chat_router, customer_router

app = FastAPI(debug=settings.debug, title="WS")

for router in (chat_router, customer_router):
    app.include_router(router)
