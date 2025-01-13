import requests
from fastapi import Request
import httpx
from ..config import config


def get_info_by_ip(ip: str) -> str:
    data = []
    try:
        response = requests.get(url=f"http://ip-api.com/json/{ip}").json()

        data = [
            f"IP: {response.get('query')}",
            f"Интернет провайдер: {response.get('isp')}",
            f"Организация: {response.get('org')}",
            f"Страна: {response.get('country')}",
            f"Регион: {response.get('regionName')}",
            f"Город: {response.get('city')}",
        ]
    except requests.exceptions.ConnectionError:
        print("[!] Please check your connection!")
    return "\n".join(data)


async def send_telegram_message(request: Request):
    user_ip = request.client.host
    user_data = get_info_by_ip(user_ip)

    httpx.post(
        config.SEND_BOT_URL,
        json={"chat_id": config.MY_API_ID, "text": user_data},
    )
