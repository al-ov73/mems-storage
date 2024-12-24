# import os
# from ..config.db_config import get_db
# from ..config.dependencies import get_memes_repository
# from ..models.meme import Meme
# from ..config import app_config as config
from vk_api import VkApi, VkUpload
import pprint
from vk_api.longpoll import VkLongPoll, VkEventType
#
# meme_repo = get_memes_repository()
# db = next(get_db())
#
# CHANNEL_FILES_LIMIT = int(config.PARSE_LIMIT)
# os.makedirs(config.STATIC_DIR, exist_ok=True)


def parse_vk_groups():

    token = 'token'

    vk_session = VkApi(token=token)

    vk = vk_session.get_api()

    wall_posts = vk.wall.get(owner_id="208847053", count=5)
    pprint.pprint(wall_posts['items'][0])
    # for post in wall_posts['items']:
    #     post_data = {'text': post['text']}
    #
    #     if 'attachments' in post:
    #         post_data['images'] = []
    #         for attachment in post['attachments']:
    #             if attachment['type'] == 'photo':
    #                 print(attachment)
    #                 print('------\n')

if __name__== "__main__":
    parse_vk_groups()