from pydantic import BaseModel
from datetime import datetime

class LabelSchema2(BaseModel):
    id: int
    title: str

class MemeDbSchema(BaseModel):
    id: int
    name: str
    created_at: datetime
    category: str
    meme_labels: list["LabelSchema2"]

class MemeSchema(MemeDbSchema):
    link: str
