from pydantic import BaseModel
from datetime import datetime


class LabelSchema(BaseModel):
    id: int
    name: str
