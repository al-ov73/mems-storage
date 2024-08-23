from abc import abstractmethod, ABC
from tempfile import SpooledTemporaryFile
from typing import BinaryIO

import aiohttp
import requests


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

    # async with aiohttp.ClientSession() as session:
    #     async with session.get('http://example.com') as resp:
    #         return await resp.text()

    async def get_link(self, image_name: str) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{self.api_url}/images/{image_name}') as resp:
                return await resp.text()

    async def add_image(self, filename: str, file: SpooledTemporaryFile) -> str:
        async with aiohttp.ClientSession() as session:
            await session.post(f'{self.api_url}/images', files={
                'file': (filename, file, 'multipart/form-data')})
            return filename

    async def delete_image(self, image_name: str) -> str:
        async with aiohttp.ClientSession() as session:
            await session.delete(f'{self.api_url}/images/{image_name}')
            return image_name

    async def update_image(self, old_name: str, new_name: str, new_file: SpooledTemporaryFile) -> str:
        async with aiohttp.ClientSession() as session:
            await session.delete(f'{self.api_url}/images/{old_name}')
            await session.post(f'{self.api_url}/images', files={
                'file': (new_name, new_file, 'multipart/form-data')
            })
            return new_name
