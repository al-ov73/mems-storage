import asyncio
from app.utils.telegram_parser import parse_telegram_channels


async def parse():
    count = await parse_telegram_channels()
    print(count)

if __name__=="__main__":
    asyncio.run(parse())
    