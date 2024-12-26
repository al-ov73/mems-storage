import os

from gigachat import GigaChat
from dotenv import load_dotenv

from fastapi import APIRouter, Form

load_dotenv()

router = APIRouter()

AUTH_KEY = os.getenv("AUTH_KEY")


@router.post("/")
async def get_data_from_form(question: str = Form()) -> str:
    print("get question: ", question)
    with GigaChat(credentials=AUTH_KEY, scope="GIGACHAT_API_PERS", verify_ssl_certs=False) as giga:
        response = giga.chat(question)
    return response.choices[0].message.content
