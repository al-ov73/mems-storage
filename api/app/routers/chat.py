from typing import List

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session

from ..repositories.messages_repository import MessagesRepository
from ..config.db_config import get_db
from ..config.dependencies import get_messages_repository
from ..models.message import Message
from ..schemas.messages import MessageSchema
from ..utils.chat_utils import ConnectionManager

router = APIRouter()

manager = ConnectionManager()


@router.get("/messages")
async def get_last_messages(
    db: Session = Depends(get_db),
    messages_repo: MessagesRepository = Depends(get_messages_repository),
) -> List[MessageSchema]:
    '''
    send all last chat messages
    '''
    messages = await messages_repo.get_messages(db)
    return messages


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    db: Session = Depends(get_db),
    messages_repo: MessagesRepository = Depends(get_messages_repository),
):
    '''
    wait message from Websocket and send it through all opened connections
    '''
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            new_message = Message(text=data['text'], author_id=data['author'])
            new_message = await messages_repo.add_message(new_message, db)
            await manager.broadcast(new_message)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast("Client left the chat")
