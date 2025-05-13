from datetime import datetime

from pydantic import BaseModel

from .users import UserSchema


class MessageSchema(BaseModel):
    id: int
    text: str
    created_at: datetime
    author: UserSchema


class SupportMessageSchema(BaseModel):
    username: str
    message: str
