import requests
import base64
import shutil
from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole
from ..config import app_config

GIGACHAT_KEY = app_config.GIGACHAT_KEY


async def get_response_from_gigachat(question: str) -> str:
    payload = Chat(
        messages=[Messages(role=MessagesRole.USER, content=question)],
        temperature=0.7,
        max_tokens=100,
        function_call="auto",
    )
    with GigaChat(credentials=GIGACHAT_KEY, verify_ssl_certs=False) as giga:
        response = giga.chat(payload)

        message_content = response.choices[0].message.content
        if '<img' in message_content:
            start_index = message_content.find('src="') + len('src="')
            end_index = message_content.find('"', start_index)
            image_id = message_content[start_index:end_index]
            image = giga.get_image(image_id)
            with open('./image.jpg', mode="wb") as fd:
                fd.write(base64.b64decode(image.content))
            print('file saved')
