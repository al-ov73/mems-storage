from pydantic import BaseModel
from datetime import datetime

# from .memes import MemeDbSchema


class CommentSchema(BaseModel):
    id: int
    text: str
    author_id: int
    created_at: datetime
    meme_id: int
