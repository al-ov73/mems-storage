from .app_config import MINIO_API_URL
from ..repositories.memes_repository import MemesRepository
from ..repositories.storage_repository import StorageRepository
from ..repositories.messages_repository import MessagesRepository


def get_memes_repository():
    return MemesRepository()


def get_storage_repo():
    return StorageRepository(MINIO_API_URL)


def get_messages_repository():
    return MessagesRepository()
