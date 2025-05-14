import base64
from dataclasses import dataclass

from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole

from ..config import config

GIGACHAT_KEY = config.GIGACHAT_KEY


@dataclass
class GigaReply:
    text_reply: str
    image: bytes | None = None


async def get_response_from_gigachat(question: str) -> GigaReply:
    payload = Chat(
        messages=[Messages(role=MessagesRole.USER, content=question)],
        temperature=0.7,
        max_tokens=100,
        function_call="auto",
    )
    image = None
    with GigaChat(credentials=GIGACHAT_KEY, verify_ssl_certs=False) as giga:
        response = giga.chat(payload)

        message = response.choices[0].message.content
        text_msg = message
        if "<img" in message:
            start_index = message.find('src="') + len('src="')
            end_index = message.find('"', start_index)
            image_id = message[start_index:end_index]
            image = giga.get_image(image_id)
            text_msg = message[end_index:]
            image = base64.b64decode(image.content)
        return GigaReply(text_reply=text_msg, image=image)
