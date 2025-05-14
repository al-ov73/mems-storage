import os

from dotenv import load_dotenv
from fastapi import APIRouter, Form
from gigachat import GigaChat
from openai import OpenAI

load_dotenv()

router = APIRouter()

AUTH_KEY = os.getenv("AUTH_KEY")


@router.post("/")
async def get_data_from_form(question: str = Form()) -> str:
    print("get question: ", question)
    with GigaChat(credentials=AUTH_KEY, scope="GIGACHAT_API_PERS", verify_ssl_certs=False) as giga:
        response = giga.chat(question)
    return response.choices[0].message.content


@router.post("/chatgpt")
async def get_data_from_chatgpt(question: str = Form()) -> str:

    print("question ", question)
    PROXY_API_KEY = ""
    proxies = {
        "http://": "http://47.247.218.29:3129",
        "https://": "https://47.247.218.29:3129",
    }
    openai_api_key = ""
    client = OpenAI(
        api_key=PROXY_API_KEY,
        base_url="https://api.proxyapi.ru/openai/v1",  # Используем httpx для прокси
    )
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Укажите модель
        messages=[{"role": "user", "content": question}],  # Ваш запрос
        max_tokens=150,  # Максимальное количество токенов в ответе
        temperature=0.7,  # Параметр "творчества" (от 0 до 1)
    )
    return response.choices[0].message.content.strip()
