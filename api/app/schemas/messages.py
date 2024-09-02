from pydantic import BaseModel
from datetime import datetime
from .users import UserSchema


class MessageSchema(BaseModel):
    id: int
    text: str
    created_at: datetime
    author: UserSchema
