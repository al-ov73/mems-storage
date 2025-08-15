from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class VisitInputSchema(BaseModel):
    ip: str
    provider: Optional[str] = None
    organization: Optional[str] = None
    country: Optional[str] = None
    region: Optional[str] = None
    city: Optional[str] = None
    landing_page: Optional[str] = "memovoz.ru"
    is_new_user: Optional[bool] = None


class VisitSchema(BaseModel):
    id: int
    ip: str
    provider: Optional[str] = None
    organization: Optional[str] = None
    country: Optional[str] = None
    region: Optional[str] = None
    city: Optional[str] = None
    visit_at: datetime
    is_new_user: Optional[bool] = None
    landing_page: Optional[str] = "memovoz.ru"

    class Config:
        from_attributes = True