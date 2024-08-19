from pydantic import BaseModel
from datetime import datetime


class MemeSchema(BaseModel):
    id: int
    name: str
    created_at: datetime
    link: str


class MemeDbSchema(BaseModel):
    id: int
    name: str
    created_at: datetime
