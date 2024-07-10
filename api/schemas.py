from datetime import datetime
from typing import List
import uuid
from pydantic import BaseModel, EmailStr, constr


class MemeBase(BaseModel):
    name: str
    url: str


class CreateMeme(MemeBase):
    name: str
    url: str


class Meme(MemeBase):
    pass
    # id: uuid.UUID
    # name: str
    # url: str
    # created_at: datetime
    
    # class Config:
    #     orm_mode = True
