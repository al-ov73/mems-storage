from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from ..config.db_config import Base
from .user import intpk


class Like(Base):
    __tablename__ = 'likes'

    id: Mapped[intpk]
    author_id: Mapped[int] = mapped_column(ForeignKey(
        'users.id', ondelete='CASCADE'), primary_key=True)
    meme_id: Mapped[int] = mapped_column(ForeignKey(
        'memes.id', ondelete='CASCADE'), primary_key=True)
    meme: Mapped['Meme'] = relationship(  # noqa: F821
        back_populates='likes'
    )
