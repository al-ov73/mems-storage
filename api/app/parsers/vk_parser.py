import logging
import os
from urllib.parse import urljoin

import requests

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

token = config.VK_TOKEN
vk_groups = config.VK_GROUPS
limit = config.PARSE_LIMIT


async def parse_vk_groups():
    for group in vk_groups:
        logger.info(f"Parsing vk group '{group}'")
        params = {"access_token": token, "v": 5.199, "domain": group, "count": limit}
        response = requests.get("https://api.vk.com/method/wall.get", params=params).json()
        posts = response["response"]["items"]
        for post in posts:
            attachments = post.get("attachments")
            for attachment in attachments:
                if attachment.get("type") == "photo":
                    img_id = attachment.get("photo").get("id")
                    filename = f"vk_{group}_{img_id}"
                    filepath = os.path.join(config.STATIC_DIR, "photos", filename)

                    if not os.path.exists(f"{filepath}.jpg"):
                        logger.info(f"Downloading {filepath}.jpg from vk group '{group}'")
                        await save_meme(attachment, filename, filepath, group)


async def save_meme(attachment, filename, filepath, group):
    with db.begin():
        preview_link = await save_meme_to_fs(attachment, filepath)
        await save_meme_to_db(filename, preview_link, group)


async def save_meme_to_db(filename, preview_link, group):
    image_link = urljoin(config.API_URL, f"{config.STATIC_URL}/photos/{filename}.jpg")
    new_meme = Meme(
        name=f"{filename}.jpg",
        source_type="vk",
        source_name=group,
        checked=False,
        link=image_link,
        preview=preview_link,
    )
    await meme_repo.add_meme(new_meme, db, commit=False)


async def save_meme_to_fs(attachment, filepath):
    img_url = attachment.get("photo").get("orig_photo").get("url")
    r = requests.get(img_url)
    with open(f"{filepath}.jpg", "wb") as f:
        f.write(r.content)
    compress_image(filepath)


if __name__ == "__main__":
    parse_vk_groups()
