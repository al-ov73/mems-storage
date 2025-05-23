import asyncio

from ..parsers.telegram_parser import parse_telegram_channels
from ..parsers.vk_parser import parse_vk_groups


async def parse():
    await parse_telegram_channels()
    await parse_vk_groups()


if __name__ == "__main__":
    asyncio.run(parse())
