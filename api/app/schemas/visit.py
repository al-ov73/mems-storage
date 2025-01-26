from pydantic import BaseModel
from datetime import datetime


class VisitInputSchema(BaseModel):
    ip: str | None
    provider: str | None
    organization: str | None
    country: str | None
    region: str | None
    city: str | None


class VisitSchema(BaseModel):
    id: int
    ip: str | None
    provider: str | None
    organization: str | None
    country: str | None
    region: str | None
    city: str | None
    visit_at: datetime
