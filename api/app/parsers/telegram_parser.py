import os
import logging
from urllib.parse import urljoin

from telethon import TelegramClient

from ..config import config as config
from ..config.db_config import get_db
from ..config.dependencies import get_memes_repository
from ..models.meme import Meme
from ..utils.os_utils import compress_image


logger = logging.getLogger(__name__)

meme_repo = get_memes_repository()
db = next(get_db())

CHANNEL_FILES_LIMIT = int(config.PARSE_LIMIT)
os.makedirs(config.STATIC_DIR, exist_ok=True)


async def parse_telegram_channels() -> None:
    async with TelegramClient(
        "session_name",
        config.API_ID,
        config.API_HASH,
        system_version="4.16.30-vxCUSTOM",
    ) as client:
        for channel in config.CHANNELS:
            try:
                logger.info(f"Parsing tg channel '{channel}'")
                messages = await client.get_messages(channel, limit=CHANNEL_FILES_LIMIT)
            except ValueError:
                continue

            for message in messages:
                if message.photo:
                    filename = f"tg_{message._chat.username}_{message.photo.id}"
                    filepath = os.path.join(
                        config.STATIC_DIR, 
                        "photos", 
                        filename
                    )
                    if not os.path.exists(f"{filepath}.jpg"):
                        logger.info(f"Downloading '{filename}.jpg' from tg channel {channel}")
                        await save_meme(client, filepath, message)


async def save_meme(client, filepath, message):
    image_link = urljoin(
        config.API_URL,
        config.STATIC_URL,
        photos,
        f"{filename}.jpg"
    )

    with db.begin():
        await client.download_media(message.photo, filepath)
        preview_link = compress_image(filepath)
        
        new_meme = Meme(
            name=f"{os.path.basename(filepath)}.jpg",
            source_type="tg",
            source_name=message._chat.username,
            checked=False,
            link=image_link,
            preview=preview_link,
        )
        await meme_repo.add_meme(new_meme, db, commit=False)
