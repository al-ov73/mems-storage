from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..config.db_config import Base
from .user import created_at, intpk


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[intpk]
    text: Mapped[str] = mapped_column(nullable=False)
    author_name: Mapped[str] = mapped_column(ForeignKey("users.username", ondelete="CASCADE"))
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    created_at: Mapped[created_at]
    meme_id: Mapped[int] = mapped_column(ForeignKey("memes.id", ondelete="CASCADE"))
    meme: Mapped["Meme"] = relationship(back_populates="comments")  # noqa: F821
