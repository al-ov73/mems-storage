from datetime import datetime

from pydantic import BaseModel


class StatSchema(BaseModel):
    total: int
    published: int
    not_published: int
    not_checked: int


class DayStatSchema(BaseModel):
    date: datetime
    count: int
