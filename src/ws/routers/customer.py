from asyncio import Queue
from typing import Annotated

from fastapi import APIRouter, Query, WebSocket, WebSocketDisconnect
from faststream.rabbit.fastapi import RabbitRouter

from src.core.config import settings
from src.schemas.customer import CustomerErrorStatusUpdate

text_queues_by_hub_id: dict[int, Queue[str]] = {}

customer_router = APIRouter()


@customer_router.websocket("/customer")
async def customer_error_status_ws(
    hub_id: Annotated[int, Query()], ws: WebSocket
) -> None:
    text_queue: Queue[str] = Queue()
    text_queues_by_hub_id[hub_id] = text_queue
    await ws.accept()
    await ws.send_text('{"status": "ok"}')
    try:
        while True:
            await ws.send_text(await text_queue.get())
    except WebSocketDisconnect:
        pass
    finally:
        del text_queues_by_hub_id[hub_id]


router = RabbitRouter(settings.rabbit.url)


@router.subscriber("customer_error_status_updates")
async def handle_customer_error_status_update(
    update: CustomerErrorStatusUpdate,
) -> None:
    text_queue = text_queues_by_hub_id.get(update.hub_id)
    if text_queue is not None:
        error_status_json = f'{{"error_status": "{update.error_status}"}}'
        await text_queue.put(error_status_json)


customer_router.include_router(router)
