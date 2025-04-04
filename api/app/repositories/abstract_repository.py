from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Optional, List, Type

from ..schemas.likes import LikeSchema
from ..models.like import Like
from ..models.comment import Comment
from ..models.label import Label
from ..models.message import Message
from ..models.user import User
from sqlalchemy.orm import Session

from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Optional, List, Type, Dict, Any
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func

T = TypeVar("T")


class IRepository(Generic[T], ABC):
    """Abstract repository interface with CRUD operations"""

    @abstractmethod
    async def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[T]:
        """Get all entities with pagination"""
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, db: Session, entity_id: str) -> Optional[T]:
        """Get single entity by ID"""
        raise NotImplementedError

    @abstractmethod
    async def create(self, db: Session, entity_data: dict) -> T:
        """Create new entity"""
        raise NotImplementedError

    @abstractmethod
    async def update(self, db: Session, entity_id: str, update_data: dict) -> Optional[T]:
        """Update existing entity"""
        raise NotImplementedError

    @abstractmethod
    async def delete(self, db: Session, entity_id: str) -> bool:
        """Delete entity by ID"""
        raise NotImplementedError


class BaseRepository(IRepository[T]):
    """Concrete repository implementation"""

    def __init__(self, entity_class: Type[T]):
        self.entity_class = entity_class

    async def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[T]:
        return db.query(self.entity_class).offset(skip).limit(limit).all()

    async def get_by_id(self, db: Session, entity_id: str) -> Optional[T]:
        return db.get(self.entity_class, entity_id)

    async def create(self, db: Session, entity_data: dict) -> T:
        entity = self.entity_class(**entity_data)
        db.add(entity)
        db.commit()
        db.refresh(entity)
        return entity

    async def update(self, db: Session, entity_id: str, update_data: dict) -> Optional[T]:
        entity = await self.get_by_id(db, entity_id)
        if entity:
            for key, value in update_data.items():
                setattr(entity, key, value)
            db.commit()
            db.refresh(entity)
        return entity

    async def delete(self, db: Session, entity_id: str) -> bool:
        entity = await self.get_by_id(db, entity_id)
        if entity:
            db.delete(entity)
            db.commit()
            return True
        return False


class LabelsRepository(BaseRepository[Label]):
    def __init__(self):
        super().__init__(Label)

    async def get_by_title(self, db: Session, title: str) -> Optional[Label]:
        return db.query(Label).filter(Label.title == title).first()

    async def create(self, db: Session, entity_data: dict) -> Label:
        # Для Label специальная логика создания, так как принимается только title
        if isinstance(entity_data, str):
            entity_data = {"title": entity_data}
        elif "title" not in entity_data:
            raise ValueError("Label requires 'title' field")

        return await super().create(db, entity_data)


class UsersRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User)

    async def get_with_relations(self, db: Session, user_id: str) -> Optional[User]:
        """Get user with all related data (messages, likes, etc.)"""
        return (
            db.query(User)
            .options(joinedload(User.messages), joinedload(User.likes), joinedload(User.comments))
            .filter(User.id == user_id)
            .first()
        )


class LikesRepository(BaseRepository[Like]):
    def __init__(self):
        super().__init__(Like)

    async def add_like(
        self,
        db: Session,
        author_id: int,
        meme_id: int,
    ) -> LikeSchema:
        """
        add like to db
        """
        new_like = Like(
            author_id=author_id,
            meme_id=meme_id,
        )
        db.add(new_like)
        db.commit()
        db.refresh(new_like)
        return new_like

    async def get_by_user_and_meme(self, db: Session, user_id: int, meme_id: int) -> Optional[Like]:
        return db.query(Like).filter(Like.author_id == user_id, Like.meme_id == meme_id).first()


class CommentsRepository(BaseRepository[Comment]):
    def __init__(self):
        super().__init__(Comment)

    async def get_by_meme(self, db: Session, meme_id: str, skip: int = 0, limit: int = 100) -> List[Comment]:
        return db.query(Comment).filter(Comment.meme_id == meme_id).offset(skip).limit(limit).all()


class MessagesRepository(BaseRepository[Message]):
    def __init__(self):
        super().__init__(Message)

    async def get_with_author(self, db: Session, message_id: str) -> Optional[Message]:
        return db.query(Message).options(joinedload(Message.author)).filter(Message.id == message_id).first()


# Фабрика репозиториев
class RepositoryFactory:
    _repositories = {
        Label: LabelsRepository,
        User: UsersRepository,
        Like: LikesRepository,
        Comment: CommentsRepository,
        Message: MessagesRepository,
    }

    @staticmethod
    def get_repository(entity_type: Type[T]) -> IRepository[T]:
        repo_class = RepositoryFactory._repositories.get(entity_type, BaseRepository)
        return repo_class()
