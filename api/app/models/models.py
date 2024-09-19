import enum

from datetime import datetime
from sqlalchemy import TIMESTAMP, Column, String, Integer, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..config.db_config import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    registered_at = Column(TIMESTAMP, default=datetime.utcnow)
    hashed_password = Column(String, nullable=False)

    memes = relationship("Meme", back_populates="author")
    messages = relationship("Message", back_populates="author")


class CategoryEnum(enum.Enum):
    OTHER = 'OTHER'
    CATS = 'CATS'
    PEOPLE = 'PEOPLE'
    IT = 'IT'


class Meme(Base):
    __tablename__ = 'memes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    author_id = Column(ForeignKey("users.id"))
    author = relationship("User", back_populates="memes")

    category = Column(Enum(CategoryEnum))

    meme_labels: Mapped[list["Label"]] = relationship(secondary="labels_meme", back_populates="label_memes")

    comments: Mapped[list["Comment"]] = relationship(back_populates="meme")

    likes: Mapped[list["Like"]] = relationship("Like", back_populates="meme")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at,
            "author_id": self.author_id,
            "category_id": self.category_id,
            "labels": self.labels,
            "comments": self.comments,
            # "likes": self.likes,
        }

class Label(Base):
    __tablename__ = 'labels'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False, unique=True)

    label_memes: Mapped[list["Meme"]] = relationship(secondary="labels_meme", back_populates="meme_labels")


class LabelMeme(Base):
    __tablename__ = "labels_meme"

    id = Column(Integer, primary_key=True)
    label_id = Column(Integer, ForeignKey('labels.id'))
    meme_id = Column(Integer, ForeignKey('memes.id'))


class Like(Base):
    __tablename__ = 'likes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    author_id = Column(ForeignKey("users.id"), primary_key=True)
    meme_id = Column(ForeignKey("memes.id"), primary_key=True)
    meme: Mapped["Meme"] = relationship(back_populates="likes")


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String, nullable=False)
    author_name = Column(ForeignKey("users.username"))
    author_id = Column(ForeignKey("users.id"))
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    meme_id: Mapped[Integer]= Column(ForeignKey('memes.id'))
    meme: Mapped["Meme"] = relationship(back_populates="comments")


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    text = Column(String)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    author_id = Column(ForeignKey("users.id"))
    author = relationship("User", back_populates="messages")

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
