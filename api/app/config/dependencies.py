from .app_congif import MINIO_API_URL
from ..repositories.memes_repository import MemesRepository
from ..repositories.storage_repository import StorageRepository


def get_memes_repository():
    return MemesRepository()


def get_storage_repo():
    return StorageRepository(MINIO_API_URL)
