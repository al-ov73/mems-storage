import enum

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Enum

from ..config.db_config import Base
from .user import intpk
from .user import created_at


class CategoryEnum(enum.Enum):
    OTHER = 'OTHER'
    CATS = 'CATS'
    PEOPLE = 'PEOPLE'
    IT = 'IT'


class Meme(Base):
    __tablename__ = 'memes'

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    created_at: Mapped[created_at]

    author_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'))
    author: Mapped['User'] = relationship(  # noqa: F821
        back_populates='memes'
    )

    category: Mapped['CategoryEnum'] = mapped_column(Enum(CategoryEnum))
    meme_labels: Mapped[list['Label']] = relationship(  # noqa: F821
        secondary='labels_meme', back_populates='label_memes')
    comments: Mapped[list['Comment']] = relationship(  # noqa: F821
        back_populates='meme'
    )
    likes: Mapped[list['Like']] = relationship(  # noqa: F821
        back_populates='meme'
    )

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at,
            'author_id': self.author_id,
            'category_id': self.category_id,
            'labels': self.labels,
            'comments': self.comments,
            'likes': self.likes,
        }
