from ..repositories.users_repository import UsersRepository
from ..config import config
from ..repositories.comments_repository import CommentsRepository
from ..repositories.memes_repository import MemesRepository
from ..repositories.storage_repository import FSStorageRepository
from ..repositories.messages_repository import MessagesRepository
from ..repositories.labels_repository import LabelsRepository
from ..repositories.likes_repository import LikesRepository


def get_memes_repository():
    return MemesRepository()


meme_repo = get_memes_repository()


def get_storage_repo():
    return FSStorageRepository(config.PHOTOS_DIR)
    # return StorageRepository(MINIO_API_URL)


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
