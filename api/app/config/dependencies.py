from ..repositories.users_repository import UsersRepository
from .app_config import MINIO_API_URL
from ..repositories.comments_repository import CommentsRepository
from ..repositories.memes_repository import MemesRepository
from ..repositories.storage_repository import StorageRepository
from ..repositories.messages_repository import MessagesRepository
from ..repositories.labels_repository import LabelsRepository
from ..repositories.likes_repository import LikesRepository


def get_memes_repository():
    return MemesRepository()


def get_storage_repo():
    return StorageRepository(MINIO_API_URL)


def get_messages_repository():
    return MessagesRepository()


def get_labels_repository():
    return LabelsRepository()


def get_comments_repository():
    return CommentsRepository()


def get_likes_repository():
    return LikesRepository()


def get_users_repository():
    return UsersRepository()
