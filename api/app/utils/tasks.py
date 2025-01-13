import requests
from fastapi import Request
import httpx
from ..config import config
from ..config.config import LOCAL_IPS


def get_info_by_ip(ip: str) -> str | None:
    data = []
    try:
        response = requests.get(url=f"http://ip-api.com/json/{ip}").json()

        if response.get('query') in LOCAL_IPS:
            return

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


async def send_user_info_to_bot(request: Request) -> None:
    user_ip = request.client.host
    user_data = get_info_by_ip(user_ip)
    if user_data:
        httpx.post(
            config.SEND_BOT_URL,
            json={"chat_id": config.MY_API_ID, "text": user_data},
        )
