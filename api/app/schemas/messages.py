from pydantic import BaseModel
from datetime import datetime


class MessagesModel(BaseModel):
    id: int
    text: str
    created_at: datetime
    author_id: str

    class Config:
        orm_mode = True