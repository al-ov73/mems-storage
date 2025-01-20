import os
from ..config.db_config import get_db
from ..config.dependencies import get_memes_repository
from ..models.meme import Meme
from ..config import config as config
from telethon import TelegramClient
from urllib.parse import urljoin

from ..utils.os_utils import compress_image

meme_repo = get_memes_repository()
db = next(get_db())

CHANNEL_FILES_LIMIT = int(config.PARSE_LIMIT)
os.makedirs(config.STATIC_DIR, exist_ok=True)


# async def parse_telegram_channels() -> None:
#     async with TelegramClient(
#         "session_name",
#         config.API_ID,
#         config.API_HASH,
#         system_version="4.16.30-vxCUSTOM",
#     ) as client:
#         for channel in config.CHANNELS:
#             print(f"trying parse tg channel {channel}")
#             try:
#                 messages = await client.get_messages(channel, limit=CHANNEL_FILES_LIMIT)
#             except ValueError:
#                 continue
#             print(f"find {len(messages)} in tg channel {channel}")
#             for message in messages:
#                 if message.photo:
#                     filename = f"tg_{message._chat.username}_{message.photo.id}"
#                     print(f"find photo {filename}")
#                     filepath = f"{config.STATIC_DIR}/photos/{filename}"
#                     if not os.path.exists(f"{filepath}.jpg"):
#                         image_link = f"{config.API_URL}/{config.STATIC_URL}/photos/{filename}.jpg"
#                         preview_link = f"{config.API_URL}/{config.STATIC_URL}/previews/{filename}.jpeg"
#                         new_meme = Meme(
#                             name=f"{filename}.jpg",
#                             source_type="tg",
#                             source_name=message._chat.username,
#                             checked=False,
#                             link=image_link,
#                             preview=preview_link,
#                         )
#                         meme_in_db = await meme_repo.add_meme(new_meme, db)
#                         await client.download_media(message.photo, filepath)
#                         preview_path = f"{config.STATIC_DIR}/previews/{filename}.jpeg"
#                         compress_image(f"{filepath}.jpg", preview_path)


async def parse_telegram_channels() -> None:
    async with TelegramClient(
        "session_name",
        config.API_ID,
        config.API_HASH,
        system_version="4.16.30-vxCUSTOM",
    ) as client:
        for channel in config.CHANNELS:
            try:
                messages = await client.get_messages(channel, limit=CHANNEL_FILES_LIMIT)
            except ValueError:
                continue

            for message in messages:
                if message.photo:
                    filename = f"tg_{message._chat.username}_{message.photo.id}"
                    filepath = os.path.join(config.STATIC_DIR, "photos", filename)
                    if not os.path.exists(f"{filepath}.jpg"):
                        image_link = urljoin(config.API_URL, f"{config.STATIC_URL}/photos/{os.path.basename(filepath)}.jpg")
                        preview_link = urljoin(config.API_URL, f"{config.STATIC_URL}/previews/{os.path.basename(filepath)}.jpeg")
                        new_meme = Meme(
                            name=f"{os.path.basename(filepath)}.jpg",
                            source_type="tg",
                            source_name=message._chat.username,
                            checked=False,
                            link=image_link,
                            preview=preview_link,
                        )
                        meme_in_db = await meme_repo.add_meme(new_meme, db)
                        if meme_in_db:
                            await client.download_media(message.photo, filepath)
                            preview_path = os.path.join(config.STATIC_DIR, "previews", f"{os.path.basename(filepath)}.jpeg")
                            compress_image(f"{filepath}.jpg", preview_path)
