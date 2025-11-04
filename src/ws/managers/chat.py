from fastapi import WebSocket

from src.schemas.chat import ChatMessage, ChatNotification
from src.ws.managers.base import AbstractConnectionManager


class ChatConnectionManager(AbstractConnectionManager):
    def __init__(self) -> None:
        self.room_connections: dict[int, set[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, chat_room_id: int) -> None:
        await websocket.accept()

        if chat_room_id not in self.room_connections:
            self.room_connections[chat_room_id] = set()

        self.room_connections[chat_room_id].add(websocket)

    async def disconnect(
        self, websocket: WebSocket, chat_room_id: int
    ) -> None:
        if chat_room_id in self.room_connections:
            self.room_connections[chat_room_id].discard(websocket)
            if not self.room_connections[chat_room_id]:
                del self.room_connections[chat_room_id]

    async def broadcast(
        self,
        websocket: WebSocket,
        message: ChatMessage,
        exclude_sender: bool = False,
    ) -> None:
        if message.chat_room_id not in self.room_connections:
            return

        disconnected_websockets = set()
        for connection in self.room_connections[message.chat_room_id]:
            if exclude_sender and connection == websocket:
                continue
            try:
                await connection.send_json(message.model_dump(mode="json"))
            except Exception:  # noqa: BLE001
                disconnected_websockets.add(connection)

        for disconnected_websocket in disconnected_websockets:
            await self.disconnect(disconnected_websocket, message.chat_room_id)


class ChatNotificationConnectionManager(AbstractConnectionManager):
    def __init__(self) -> None:
        self.connections: set[WebSocket] = set()

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.connections.add(websocket)

    async def disconnect(self, websocket: WebSocket) -> None:
        self.connections.discard(websocket)

    async def broadcast(self, notification: ChatNotification) -> None:
        disconnected_websockets = set()
        for connection in self.connections:
            try:
                await connection.send_json(
                    notification.model_dump(mode="json")
                )
            except Exception:  # noqa: BLE001
                disconnected_websockets.add(connection)

        for disconnected_websocket in disconnected_websockets:
            await self.disconnect(disconnected_websocket)


chat_connection_manager = ChatConnectionManager()
chat_notification_connection_manager = ChatNotificationConnectionManager()
