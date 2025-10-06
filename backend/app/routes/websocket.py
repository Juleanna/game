from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from typing import Dict, List
import json
from app.core.dependencies import get_current_user_ws
from app.models.user import User


router = APIRouter()


class ConnectionManager:
    """Менеджер WebSocket соединений"""

    def __init__(self):
        self.active_connections: Dict[int, WebSocket] = {}  # user_id -> WebSocket

    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: int):
        if user_id in self.active_connections:
            del self.active_connections[user_id]

    async def send_personal_message(self, message: dict, user_id: int):
        if user_id in self.active_connections:
            await self.active_connections[user_id].send_json(message)

    async def broadcast(self, message: dict, exclude_user: int = None):
        """Отправить сообщение всем подключенным пользователям"""
        for user_id, connection in self.active_connections.items():
            if exclude_user and user_id == exclude_user:
                continue
            try:
                await connection.send_json(message)
            except:
                pass


manager = ConnectionManager()


@router.websocket("/ws/{token}")
async def websocket_endpoint(websocket: WebSocket, token: str):
    """WebSocket endpoint для real-time коммуникации"""

    # Валидация токена
    user = await get_current_user_ws(token)
    if not user:
        await websocket.close(code=1008)
        return

    await manager.connect(websocket, user.id)

    # Уведомление о подключении
    await manager.broadcast(
        {
            "type": "user_connected",
            "username": user.username,
            "user_id": user.id,
        },
        exclude_user=user.id,
    )

    try:
        while True:
            # Получение сообщения от клиента
            data = await websocket.receive_json()
            message_type = data.get("type")

            if message_type == "chat":
                # Чат сообщение
                await manager.broadcast(
                    {
                        "type": "chat",
                        "user": user.username,
                        "text": data.get("text", ""),
                    }
                )

            elif message_type == "move":
                # Движение персонажа
                await manager.broadcast(
                    {
                        "type": "player_moved",
                        "user_id": user.id,
                        "character_id": data.get("character_id"),
                        "x": data.get("x"),
                        "y": data.get("y"),
                    },
                    exclude_user=user.id,
                )

            elif message_type == "ping":
                # Heartbeat
                await manager.send_personal_message({"type": "pong"}, user.id)

    except WebSocketDisconnect:
        manager.disconnect(user.id)
        await manager.broadcast(
            {
                "type": "user_disconnected",
                "username": user.username,
                "user_id": user.id,
            }
        )
