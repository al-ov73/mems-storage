from aiogram import Bot
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

from ..config.config import MY_API_ID, NOT_CHECKED_URL
from ..config.db_config import db
from ..config.dependencies import meme_repo


async def send_reminder(bot: Bot, data: dict):
    user_id = data["user_id"]
    text = data["text"]
    await bot.send_message(user_id, text)


def notchecked_keyboard(notchecked_count: int) -> InlineKeyboardButton:
    builder = InlineKeyboardBuilder()
    builder.button(text=f"Проверить {notchecked_count} шт.", web_app=WebAppInfo(url=NOT_CHECKED_URL))
    return builder.as_markup(resize_keyboard=True)

async def send_day_stat(bot: Bot, stat: str):
    day_stat = await meme_repo.get_published_stat(db=db)
    await bot.send_message(MY_API_ID, stat, reply_markup=notchecked_keyboard(day_stat.not_checked))
