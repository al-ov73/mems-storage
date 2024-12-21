from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.filters.command import Command
from aiogram.types import Message
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import FSInputFile, InputFile, URLInputFile

import asyncio

from ..config.db_config import get_db
from ..config.dependencies import get_memes_repository
from ..utils.other_utils import get_folder_size
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import os
from ..config import app_config as config
from ...parse import parse


bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

meme_repo = get_memes_repository()
db = next(get_db())

async def send_photo_periodically():
    random_image = await meme_repo.get_random_meme(db=db)
    await bot.send_photo(config.CHAT_ID, URLInputFile(random_image.link))
    await meme_repo.make_meme_published(random_image.id, db)


async def parse_periodically():
    count_before = len(os.listdir(path=f"{config.STATIC_DIR}/photos"))
    folder_size_before = get_folder_size(f"{config.STATIC_DIR}/photos")
    await bot.send_message(config.MY_API_ID, "Скачиваем картинки")
    await parse()
    count_after = len(os.listdir(path=f"{config.STATIC_DIR}/photos"))
    await bot.send_message(
        config.MY_API_ID, f"Скачалось картинок: {count_after - count_before} ({count_before}->{count_after})"
    )
    folder_size_after = get_folder_size(f"{config.STATIC_DIR}/photos")
    await bot.send_message(
        config.MY_API_ID, f"Общий объем директории с мемами: {folder_size_before}МБ -> {folder_size_after}МБ"
    )


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")
    # test_kb = InlineKeyboardMarkup()
    # test_kb_1 = InlineKeyboardButton(text="Первая кнопка", callback_data="first_one")
    # test_kb.add(test_kb_1)
    # await message.answer("Кнопки:", reply_markup=test_kb)


@dp.message(Command("parse"))
async def parse_command(message: Message):
    await parse_periodically()

@dp.message(Command("send"))
async def image_send_command(message: Message):
    await send_photo_periodically()

@dp.message(Command("stat"))
async def parse_command(message: Message):
    # image_count = len(os.listdir(path=f"{config.STATIC_DIR}/photos"))

    total, published, not_published = await meme_repo.get_published_stat(db=db)
    await message.answer(f"Всего картинок: {total}")
    await message.answer(f"Опубликовано картинок: {published}")
    await message.answer(f"Не опубликовано: {not_published}")

    folder_size = get_folder_size(f"{config.STATIC_DIR}/photos")
    await message.answer(f"Общий объем директории с мемами: {folder_size}МБ")

async def start_bot():
    if config.ENV == "prod":
        scheduler = AsyncIOScheduler()
        scheduler.add_job(send_photo_periodically, "interval", minutes=int(config.SEND_PHOTO_INTERVAL))
        scheduler.add_job(parse_periodically, "interval", hours=int(config.PARSE_INTERVAL))
        scheduler.start()

    loop = asyncio.get_event_loop()
    loop.create_task(dp.start_polling(bot))
