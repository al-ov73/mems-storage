from datetime import datetime

from pydantic import BaseModel


class CommentSchema(BaseModel):
    id: int
    text: str
    author_id: int
    created_at: datetime
    meme_id: int
