import asyncio
import aiohttp


from abc import abstractmethod, ABC
from tempfile import SpooledTemporaryFile
from typing import BinaryIO

from ..config.redis_config import get_redis


class BaseStorageRepo(ABC):
    @abstractmethod
    async def get_link(self, image_name: str) -> str:
        pass

    @abstractmethod
    async def add_image(self, filename: str, file: BinaryIO) -> str:
        pass

    @abstractmethod
    async def delete_image(self, image_name: str) -> str:
        pass

    @abstractmethod
    async def update_image(self, old_name: str, new_name: str, new_file: BinaryIO) -> str:
        pass


class StorageRepository(BaseStorageRepo):
    def __init__(self, api_url):
        self.api_url = api_url

    async def get_link(
            self,
            image_name: str,
    ) -> str:
        redis = get_redis()
        cache = await redis.get(image_name)
        if cache is not None:
            return cache[1:-1]

        async with aiohttp.ClientSession() as session:
            async with session.get(f'{self.api_url}/images/{image_name}') as resp:
                link = await resp.text()
                await redis.set(image_name, link)
                return link[1:-1]

    async def add_image(self, filename: str, file: SpooledTemporaryFile) -> str:
        async with aiohttp.ClientSession() as session:
            await session.post(f'{self.api_url}/images', data={
                'file': (filename, file, 'multipart/form-data')})
            return filename

    async def delete_image(self, image_name: str) -> str:
        async with aiohttp.ClientSession() as session:
            await session.delete(f'{self.api_url}/images/{image_name}')
            return image_name

    async def update_image(self, old_name: str, new_name: str, new_file: SpooledTemporaryFile) -> str:
        async with aiohttp.ClientSession() as session:
            await session.delete(f'{self.api_url}/images/{old_name}')
            await session.post(f'{self.api_url}/images', data={
                'file': (new_name, new_file, 'multipart/form-data')
            })
            return new_name
