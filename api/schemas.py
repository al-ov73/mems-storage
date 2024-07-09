from datetime import datetime
from typing import List
import uuid
from pydantic import BaseModel, EmailStr, constr


class MemeBaseSchema(BaseModel):
    name: str
    url: str
    class Config:
        orm_mode = True


class CreateMemeSchema(MemeBaseSchema):
    pass

class MemeResponse(MemeBaseSchema):
    id: uuid.UUID
    name: str
    url: str
    created_at: datetime
