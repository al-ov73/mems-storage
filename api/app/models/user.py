from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import func
from typing import Annotated, Optional

import datetime
from ..config.db_config import Base


intpk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]
created_at = Annotated[
    datetime.datetime, mapped_column(server_default=func.now())
]


class User(Base):
    __tablename__ = "users"

    id: Mapped[intpk]
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    first_name: Mapped[Optional[str]]
    last_name: Mapped[Optional[str]]
    registered_at: Mapped[created_at]
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    memes: Mapped["Meme"] = relationship(  # noqa: F821
        back_populates="author"
    )
    messages: Mapped["Message"] = relationship(  # noqa: F821
        back_populates="author"
    )
