from datetime import datetime

from pydantic import BaseModel


class StatSchema(BaseModel):
    total: int
    published: int
    not_published: int
    not_checked: int


class MemesDayStatSchema(BaseModel):
    date: datetime
    count: int


class VisitsDayStatSchema(BaseModel):
    date: datetime
    total: int
    new_users: int
    old_users: int


class SourceStatSchema(BaseModel):
    source_name: str
    source_type: str
    count: int
