from ..database.database import Base
from sqlalchemy import TIMESTAMP, Column, String, text, \
    Integer


class Meme(Base):
    __tablename__ = 'memes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at,
        }
