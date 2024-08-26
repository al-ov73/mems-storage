from typing import List


from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.models import Messages

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

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


# @router.get("/last_messages")
# async def get_last_messages(
#         session: AsyncSession = Depends(get_async_session),
# ) -> List[MessagesModel]:
#     query = select(Messages).order_by(Messages.id.desc()).limit(5)
#     messages = await session.execute(query)
#     return messages.scalars().all()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    print('websocket', websocket)
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print('received message ->', data)
            # await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client left the chat")