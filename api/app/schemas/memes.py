from pydantic import BaseModel
from datetime import datetime


class MemeDbSchema(BaseModel):
    id: int
    name: str
    created_at: datetime
    category: str


class MemeSchema(MemeDbSchema):
    link: str
