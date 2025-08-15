from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column

from ..config.db_config import Base
from .user import created_at, intpk
from ..schemas.visit import VisitInputSchema


class Visit(Base):
    __tablename__ = "visits"

    id: Mapped[intpk]
    ip: Mapped[str]
    provider: Mapped[Optional[str]]
    organization: Mapped[Optional[str]]
    country: Mapped[Optional[str]]
    region: Mapped[Optional[str]]
    city: Mapped[Optional[str]]
    visit_at: Mapped[created_at]
    is_new_user: Mapped[Optional[bool]]
    landing_page: Mapped[Optional[str]] = mapped_column(default="memovoz.ru", nullable=True)

    @classmethod
    def from_schema(cls, schema: VisitInputSchema) -> "Visit":
        """Создает модель из схемы"""
        return cls(
            ip=schema.ip,
            provider=schema.provider,
            organization=schema.organization,
            country=schema.country,
            region=schema.region,
            city=schema.city,
            landing_page=schema.landing_page,
            is_new_user=schema.is_new_user
        )