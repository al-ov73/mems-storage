from datetime import datetime
from pydantic import BaseModel


class Meme(BaseModel):
    id: int
    name: str
    created_at: datetime
    link: str


class MemeWithLink(Meme):
    id: int
    name: str
    link: str
    created_at: datetime
