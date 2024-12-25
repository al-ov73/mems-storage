from gigachat import GigaChat
from ..config import app_config

GIGACHAT_KEY = app_config.GIGACHAT_KEY


async def get_response_from_gigachat(question: str) -> str:
    with GigaChat(credentials=GIGACHAT_KEY, scope="GIGACHAT_API_PERS", verify_ssl_certs=False) as giga:
        response = giga.chat(question)
    return response.choices[0].message.content
