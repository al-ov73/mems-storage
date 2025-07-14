from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column

from ..config.db_config import Base
from .user import created_at, intpk


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
