from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from ..config.db_config import Base
from .user import intpk
from .user import created_at


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[intpk]
    text: Mapped[str]
    created_at: Mapped[created_at]
    author_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"))
    author: Mapped["User"] = relationship(  # noqa: F821
        back_populates="messages")

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "created_at": self.created_at.isoformat(),
            "author": {
                "username": self.author.username,
                "id": self.author.id,
            },
        }
