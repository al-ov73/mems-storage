from typing import List
import json

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from ..repositories.messages_repository import MessagesRepository
from ..config.db_config import get_db
from ..config.dependencies import get_messages_repository
from ..models.models import Message
from ..schemas.messages import MessageSchema

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: MessageSchema):
        for connection in self.active_connections:
            await connection.send_json(message.to_dict())


manager = ConnectionManager()

@router.get("/messages")
async def get_last_messages(
    db: Session = Depends(get_db),
    messages_repo: MessagesRepository = Depends(get_messages_repository),
) -> List[MessageSchema]:
    messages = await messages_repo.get_messages(db)
    return messages


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    db: Session = Depends(get_db),
    messages_repo: MessagesRepository = Depends(get_messages_repository),
):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            new_message = Message(text=data['text'], author_id=data['author'])
            new_message = await messages_repo.add_message(new_message, db)
            await manager.broadcast(new_message)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client left the chat")
