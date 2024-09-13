from redis import asyncio as aioredis
from .app_config import REDIS_URL


def get_redis():
    return aioredis.from_url(REDIS_URL, encoding="utf8", decode_responses=True)
