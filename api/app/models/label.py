from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from ..config.db_config import Base
from .user import intpk


class Label(Base):
    __tablename__ = 'labels'

    id: Mapped[intpk]
    title: Mapped[str] = mapped_column(nullable=False, unique=True)
    label_memes: Mapped[list['Meme']] = relationship(  # noqa: F821
        secondary='labels_meme', back_populates='meme_labels'
    )


class LabelMeme(Base):
    __tablename__ = 'labels_meme'

    id: Mapped[intpk]
    label_id: Mapped[int] = mapped_column(
        ForeignKey('labels.id', ondelete='CASCADE'))
    meme_id: Mapped[int] = mapped_column(
        ForeignKey('memes.id', ondelete='CASCADE'))
