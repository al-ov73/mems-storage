from pydantic import BaseModel
from datetime import datetime

from .comments import CommentSchema
from .labels import LabelSchema
from .users import UserSchema


class MemeDbSchema(BaseModel):
    id: int
    name: str
    author: UserSchema
    created_at: datetime
    category: str
    meme_labels: list[LabelSchema]
    comments: list[CommentSchema]


class MemeSchema(MemeDbSchema):
    link: str
