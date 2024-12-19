from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.filters.command import Command
from aiogram.types import Message
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import FSInputFile

import random
import asyncio
from ..utils.other_utils import get_folder_size
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import os
from ..config import app_config as config
from ...parse import parse


bot = Bot(
    token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()


async def send_photo_periodically():
    images = os.listdir(path=f"{config.STATIC_DIR}/photos")
    random_image = random.choice(images)
    await bot.send_photo(
        config.CHAT_ID, FSInputFile(f"{config.STATIC_DIR}/photos/{random_image}")
    )


async def parse_periodically():
    count_before = len(os.listdir(path=f"{config.STATIC_DIR}/photos"))
    folder_size_before = get_folder_size(f"{config.STATIC_DIR}/photos")
    await bot.send_message(config.MY_API_ID, "Скачиваем картинки")
    await parse()
    count_after = len(os.listdir(path=f"{config.STATIC_DIR}/photos"))
    await bot.send_message(
        config.MY_API_ID, f"Скачалось {count_after - count_before} картинок ({count_before}->{count_after})"
    )
    folder_size_after = get_folder_size(f"{config.STATIC_DIR}/photos")
    await bot.send_message(
        config.MY_API_ID, f"Общий объем директории с мемами: {folder_size_before}МБ -> {folder_size_after / 10^6}МБ"
    )


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")
    test_kb = InlineKeyboardMarkup()
    test_kb_1 = InlineKeyboardButton(text="Первая кнопка", callback_data="first_one")
    test_kb.add(test_kb_1)
    await message.answer("Кнопки:", reply_markup=test_kb)


@dp.message(Command("parse"))
async def parse_command(message: Message):
    count_before = len(os.listdir(path=f"{config.STATIC_DIR}/photos"))
    await message.answer("Скачиваем картинки")
    await parse()
    count_after = len(os.listdir(path=f"{config.STATIC_DIR}/photos"))
    await message.answer(f"Скачалось {count_after - count_before} картинок")
    folder_size = get_folder_size(f"{config.STATIC_DIR}/photos") / 10**6
    await message.answer(f"Общий объем директории с мемами: {round(folder_size, 1)}МБ")


@dp.message(Command("stat"))
async def parse_command(message: Message):
    image_count = len(os.listdir(path=f"{config.STATIC_DIR}/photos"))
    await message.answer(f"картинок сейчас: {image_count}")


async def start_bot():
    if config.ENV == "prod":
        scheduler = AsyncIOScheduler()
        scheduler.add_job(
            send_photo_periodically, "interval", minutes=int(config.SEND_PHOTO_INTERVAL)
        )
        scheduler.add_job(parse_periodically, "interval", hours=int(config.PARSE_INTERVAL))
        scheduler.start()

    loop = asyncio.get_event_loop()
    loop.create_task(dp.start_polling(bot))
