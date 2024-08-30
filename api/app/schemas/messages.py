from pydantic import BaseModel
from datetime import datetime


class MessageSchema(BaseModel):
    id: int
    text: str
    created_at: datetime
    author_id: int
