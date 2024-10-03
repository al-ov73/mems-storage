import aiohttp
import httpx
from aiohttp import FormData, StreamReader
from abc import abstractmethod, ABC
from tempfile import SpooledTemporaryFile
from typing import BinaryIO

from ..config.logger_config import get_logger
from ..config.redis_config import get_redis

logger = get_logger(__name__)


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
    async def update_image(
        self, old_name: str, new_name: str, new_file: BinaryIO
    ) -> str:
        pass


class StorageRepository(BaseStorageRepo):
    def __init__(self, api_url):
        self.api_url = api_url

    async def get_link(
        self,
        file_id: int,
    ) -> str:
        filename = str(file_id)
        redis = get_redis()
        cache = await redis.get(filename)
        if cache is not None:
            logger.info(f"Link for image {filename} from cache")
            return cache
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.api_url}/images/link/{filename}"
            ) as resp:
                link = await resp.text()
                logger.info(
                    f"Link for image {filename} from S3 service"
                )
                await redis.set(filename, link)
                return link

    async def get_image(
        self,
        file_id: int,
    ) -> StreamReader:
        filename = str(file_id)
        response = httpx.get(f"{self.api_url}/images/{filename}")
        return response.content

    async def add_image(
            self,
            filename: str,
            file: SpooledTemporaryFile
    ) -> str:
        async with aiohttp.ClientSession() as session:
            data = FormData()
            data.add_field(
                "file",
                file,
                filename=filename,
                content_type="multipart/form-data"
            )
            logger.info("Send post request to S3 service")
            response = await session.post(f"{self.api_url}/images", data=data)
            text_response = await response.text()
            logger.info(f"Response from S3 service: {text_response}")
            return text_response

    async def delete_image(self, file_id: int) -> str:
        async with aiohttp.ClientSession() as session:
            filename = str(file_id)
            response = await session.delete(
                f"{self.api_url}/images/{filename}"
            )
            text_response = await response.text()
            return text_response

    async def update_image(
        self, old_name: str, new_name: str, new_file: SpooledTemporaryFile
    ) -> str:
        async with aiohttp.ClientSession() as session:
            await session.delete(f"{self.api_url}/images/{old_name}")
            await session.post(
                f"{self.api_url}/images",
                data={"file": (new_name, new_file, "multipart/form-data")},
            )
            return new_name
