import datetime
from typing import Annotated, Optional

from sqlalchemy import Boolean, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..config.db_config import Base

intpk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]
created_at = Annotated[datetime.datetime, mapped_column(server_default=func.now())]


class User(Base):
    __tablename__ = "users"

    id: Mapped[intpk]

    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    first_name: Mapped[Optional[str]]
    last_name: Mapped[Optional[str]]
    registered_at: Mapped[created_at]
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    messages: Mapped["Message"] = relationship(back_populates="author")
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
