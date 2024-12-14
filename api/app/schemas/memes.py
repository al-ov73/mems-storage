from pydantic import BaseModel
from datetime import datetime

from .comments import CommentSchema
from .labels import LabelSchema
from .likes import LikeSchema
from .users import UserSchema


class MemeDbSchema(BaseModel):
    id: int
    source_type: str
    source_name: str
    created_at: datetime
    category: str
    meme_labels: list[LabelSchema]
    likes: list[LikeSchema]
    comments: list[CommentSchema]
