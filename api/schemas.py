from datetime import datetime
import uuid
from pydantic import BaseModel


class Meme(BaseModel):
    id: uuid.UUID
    name: str
    url: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class CreateMeme(BaseModel):
    name: str
    url: str
