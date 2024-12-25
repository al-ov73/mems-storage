import asyncio

from .app.parsers.vk_parser import parse_vk_groups
from .app.parsers.telegram_parser import parse_telegram_channels


async def parse():
    # await parse_telegram_channels()
    await parse_vk_groups()


if __name__ == "__main__":
    asyncio.run(parse())
