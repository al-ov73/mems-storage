from pydantic import BaseModel
from datetime import datetime


class CommentSchema(BaseModel):
    id: int
    text: str
    author_id: int
    created_at: datetime
    meme_id: int
