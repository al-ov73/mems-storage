import logging

import requests
from ..schemas.messages import SupportMessageSchema
from fastapi import Request
import httpx
from ..config import config
from ..config.db_config import db
from ..config.dependencies import get_visit_repository
from ..models.visit import Visit
from ..schemas.visit import VisitInputSchema

logger = logging.getLogger(__name__)

visit_repo = get_visit_repository()


def get_text_info_by_ip(ip: str) -> str | None:
    data = []
    try:
        response = requests.get(url=f"http://ip-api.com/json/{ip}").json()

        ip = response.get("query")
        if ip in config.LOCAL_IPS:
            return

        data = [
            f"IP: {ip}",
            f"Интернет провайдер: {response.get('isp')}",
            f"Организация: {response.get('org')}",
            f"Страна: {response.get('country')}",
            f"Регион: {response.get('regionName')}",
            f"Город: {response.get('city')}",
        ]
    except requests.exceptions.ConnectionError:
        print("[!] Please check your connection!")
    return "\n".join(data)


def get_info_by_ip(ip: str) -> VisitInputSchema | None:
    try:
        response = requests.get(url=f"http://ip-api.com/json/{ip}").json()

        ip = response.get("query")
        if ip in config.LOCAL_IPS:
            return

        return Visit(
            ip=ip,
            provider=response.get("isp"),
            organization=response.get("org"),
            country=response.get("country"),
            region=response.get("regionName"),
            city=response.get("city"),
        )

    except requests.exceptions.ConnectionError:
        print("[!] Please check your connection!")


async def send_user_info_to_bot(request: Request) -> None:
    user_ip = request.client.host
    user_data = get_info_by_ip(user_ip)
    if user_data:
        httpx.post(
            config.SEND_BOT_URL,
            json={"chat_id": config.MY_API_ID, "text": user_data},
        )


async def send_visit_info_to_db(request: Request) -> None:

    user_ip = request.client.host
    logger.info(f"New visit from ip: {user_ip}")
    user_data = get_info_by_ip(user_ip)
    if user_data:
        new_visit = await visit_repo.add_visit(user_data, db)
        logger.info(f"New visit registered. Id: {new_visit.id}, is_new_user: {new_visit.is_new_user}")
    else:
        logger.info(f"New visit from config.LOCAL_IPS. Id: {user_ip}")


async def send_support_msg_to_bot(message: SupportMessageSchema) -> None:
    text_msg = f'Юзер "{message.username}" отправил сообщение:\n{message.message}'
    httpx.post(
        config.SEND_BOT_URL,
        json={"chat_id": config.MY_API_ID, "text": text_msg},
    )
