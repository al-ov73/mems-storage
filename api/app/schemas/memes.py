from datetime import datetime

from pydantic import BaseModel

from .comments import CommentSchema
from .labels import LabelSchema
from .likes import LikeSchema


class MemeDbSchema(BaseModel):
    id: int
    source_type: str
    source_name: str
    created_at: datetime
    meme_labels: list[LabelSchema]
    likes: list[LikeSchema]
    comments: list[CommentSchema]
    published: bool
    checked: bool
