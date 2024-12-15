from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..config.db_config import Base
from .user import intpk
from .user import created_at


class Meme(Base):
    __tablename__ = 'memes'

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(nullable=False)
    source_name: Mapped[str] = mapped_column(nullable=True)
    source_type: Mapped[str] = mapped_column(nullable=True)
    link: Mapped[str] = mapped_column(unique=True, nullable=False)
    created_at: Mapped[created_at]

    meme_labels: Mapped[list['Label']] = relationship(secondary='labels_meme', back_populates='label_memes')
    comments: Mapped[list['Comment']] = relationship(back_populates='meme')
    likes: Mapped[list['Like']] = relationship(back_populates='meme')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'source_name': self.source_name,
            'source_type': self.source_type,
            'link': self.link,
            'created_at': self.created_at,
            'labels': self.labels,
            'comments': self.comments,
            'likes': self.likes,
        }
