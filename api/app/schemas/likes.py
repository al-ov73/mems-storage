from pydantic import BaseModel
from datetime import datetime


class LikeSchema(BaseModel):
    id: int
    author_id: int
    meme_id: int
