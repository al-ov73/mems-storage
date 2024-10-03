from pydantic import BaseModel


class LabelSchema(BaseModel):
    id: int
    title: str
