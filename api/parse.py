import asyncio
from .app.parsers.telegram_parser import parse_telegram_channels


async def parse():
    await parse_telegram_channels()

if __name__=="__main__":
    asyncio.run(parse())
    