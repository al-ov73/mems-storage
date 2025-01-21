import os

from ..utils.os_utils import compress_image
from ..config.db_config import get_db
from ..config.dependencies import get_memes_repository
from ..models.meme import Meme
from ..config import config as config

import requests

meme_repo = get_memes_repository()
db = next(get_db())

CHANNEL_FILES_LIMIT = int(config.PARSE_LIMIT)
os.makedirs(config.STATIC_DIR, exist_ok=True)

token = config.VK_TOKEN
vk_groups = config.VK_GROUPS
limit = config.PARSE_LIMIT


async def parse_vk_groups():
    for group in vk_groups:
        params = {"access_token": token, "v": 5.199, "domain": group, "count": limit}
        response = requests.get("https://api.vk.com/method/wall.get", params=params).json()
        posts = response["response"]["items"]
        for post in posts:
            attachments = post.get("attachments")
            for attachment in attachments:
                if attachment.get("type") == "photo":
                    img_id = attachment.get("photo").get("id")
                    filename = f"vk_{group}_{img_id}"
                    filepath = f"{config.STATIC_DIR}/photos/{filename}"

                    if not os.path.exists(f"{filepath}.jpg"):

                        # save meme in filesystem
                        img_url = attachment.get("photo").get("orig_photo").get("url")
                        r = requests.get(img_url)
                        with open(f"{filepath}.jpg", "wb") as f:
                            f.write(r.content)
                        # save meme in database
                        image_link = f"{config.API_URL}/{config.STATIC_URL}/photos/{filename}.jpg"
                        preview_link = f"{config.API_URL}/{config.STATIC_URL}/previews/{filename}.jpeg"
                        new_meme = Meme(
                            name=f"{filename}.jpg",
                            source_type="vk",
                            source_name=group,
                            checked=False,
                            link=image_link,
                            preview=preview_link,
                        )
                        meme_in_db = await meme_repo.add_meme(new_meme, db)
                        preview_path = f"{config.STATIC_DIR}/previews/{filename}.jpeg"
                        compress_image(f"{filepath}.jpg", preview_path)


if __name__ == "__main__":
    parse_vk_groups()
