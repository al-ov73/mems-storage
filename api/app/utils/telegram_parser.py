import os
from app.config.db_config import get_db
from app.config.dependencies import get_memes_repository
from app.models.meme import Meme
from app.config import app_config as config
from app.config.app_config import STATIC_FILES
from telethon import TelegramClient

meme_repo = get_memes_repository()
db = next(get_db())

DOWNLOAD_PATH = STATIC_FILES
CHANNEL_FILES_LIMIT = 2
os.makedirs(DOWNLOAD_PATH, exist_ok=True)

async def parse_telegram_channels() -> None:
    async with TelegramClient('session_name', config.API_ID, config.API_HASH,
                              system_version='4.16.30-vxCUSTOM') as client:
        for channel in config.CHANNELS:
            try:
                messages = await client.get_messages(channel, limit=CHANNEL_FILES_LIMIT)
            except ValueError:
                continue
            for message in messages:
                if message.photo:
                    filename = f"tg_{message._chat.username}_{message.photo.id}"
                    filepath = f"{DOWNLOAD_PATH}{filename}"
                    if not os.path.exists(f"{filepath}.jpg"):
                        new_meme = Meme(
                            name=filename,
                            link=f"http://45.80.71.178:8000/static/photos/{filename}.jpg",
                        )
                        meme_in_db = await meme_repo.add_meme(new_meme, db)
                        print(f"meme {meme_in_db} added to db")
                        await client.download_media(message.photo, filepath)
                        print(f"file {filepath} downloaded")
