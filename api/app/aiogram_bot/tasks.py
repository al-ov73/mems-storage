from aiogram import Bot

from ..config.config import MY_API_ID


async def send_reminder(bot: Bot, data: dict):
    user_id = data["user_id"]
    text = data["text"]
    await bot.send_message(user_id, text)


async def send_day_stat(bot: Bot, stat: str):
    await bot.send_message(MY_API_ID, stat)
