from ..models.user import User
from ..models.like import Like
from ..models.label import Label
from ..models.comment import Comment
from ..repositories.abstract_repository import RepositoryFactory
from ..repositories.users_repository import UsersRepository
from ..config import config
from ..repositories.comments_repository import CommentsRepository
from ..repositories.memes_repository import MemesRepository
from ..repositories.storage_repository import FSStorageRepository
from ..repositories.messages_repository import MessagesRepository
from ..repositories.labels_repository import LabelsRepository
from ..repositories.likes_repository import LikesRepository
from ..repositories.visit_repository import VisitRepository
from ..models.message import Message


def get_memes_repository():
    return MemesRepository()


meme_repo = get_memes_repository()


def get_storage_repo():
    return FSStorageRepository(config.PHOTOS_DIR)
    # return StorageRepository(MINIO_API_URL)


def get_messages_repository():
    # return RepositoryFactory().get_repository(Message)
    return MessagesRepository()


def get_labels_repository():
    # return RepositoryFactory().get_repository(Label)
    return LabelsRepository()


def get_comments_repository():
    # return RepositoryFactory().get_repository(Comment)
    return CommentsRepository()


def get_likes_repository():
    # return RepositoryFactory().get_repository(Like)
    return LikesRepository()


def get_users_repository():
    # return RepositoryFactory().get_repository(User)
    return UsersRepository()


def get_visit_repository():
    return VisitRepository()


visit_repo = get_visit_repository()
