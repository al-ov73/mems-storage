import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import URLInputFile, Message, BufferedInputFile
from aiogram.utils.chat_action import ChatActionSender
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from .commands import bot_commands
from ..config import config
from ..config.db_config import db
from ..config.dependencies import meme_repo
from ..utils.gigachat import get_response_from_gigachat
from ..utils.os_utils import get_folder_size
from ..utils.stat_utils import format_day_stat
from ...parse import parse

bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


async def send_photo_periodically():
    random_image = await meme_repo.get_random_meme(db=db)
    await bot.send_photo(config.CHAT_ID, URLInputFile(random_image.link))
    await meme_repo.make_meme_published(random_image.id, db)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {message.from_user.full_name}!")


@dp.message(Command(commands=['parse']))
async def parse_command(message: Message):
    count_before = len(os.listdir(path=f"{config.STATIC_DIR}/photos"))
    folder_size_before = get_folder_size(f"{config.STATIC_DIR}/photos")
    reply = await bot.send_message(config.MY_API_ID, "Скачиваем картинки")
    await parse()
    count_after = len(os.listdir(path=f"{config.STATIC_DIR}/photos"))
    folder_size_after = get_folder_size(f"{config.STATIC_DIR}/photos")
    await bot.edit_message_text(
        text=f"Общий объем директории с мемами: {folder_size_before}МБ -> {folder_size_after}МБ\nСкачалось картинок: {count_after - count_before} ({count_before}->{count_after})",
        chat_id=reply.chat.id,
        message_id=reply.message_id,
    )


@dp.message(Command(commands=['send']))
async def image_send_command(message: Message):
    await send_photo_periodically()
    await message.answer("Мем отправлен")


@dp.message(Command(commands=['stat']))
async def stat_command(message: Message):
    day_stat = await meme_repo.get_published_stat(db=db)
    folder_size = get_folder_size(f"{config.STATIC_DIR}/photos")
    days_remain = (day_stat.not_published * int(config.SEND_PHOTO_INTERVAL)) / (60 * 24)
    day_stats = await meme_repo.get_memes_count_by_day(db=db)
    formated_day_stat = await format_day_stat(day_stats)
    await bot.send_message(
        config.MY_API_ID,
        f"Всего картинок: {day_stat.total} шт.\n"
        f"Опубликовано картинок: {day_stat.published} шт.\n"
        f"Не опубликовано: {day_stat.not_published} шт. ({round(days_remain)} дн.)\n"
        f"Ожидают проверки: {day_stat.not_checked} шт. <a href='http://45.80.71.178/temp'>Проверить</a>\n"
        f"Общий объем мемов: {folder_size}МБ\n\n"
        f"{formated_day_stat}",
    )

@dp.message(Command(commands=['sources']))
async def sources_command(message: Message):
    days_limit = 5
    sources_stat = await meme_repo.get_sources_stat(db=db, limit=days_limit)
    formated_stat = [f"({stat.source_type}) {stat.source_name} - {stat.count} шт.\n" for stat in sources_stat]
    await message.reply(
        f"Статистика за последние {days_limit} дн.\n"
        f"{''.join(formated_stat)}"
    )

@dp.message()
async def other_command(message: Message) -> None:
    giga_reply = await get_response_from_gigachat(message.text)
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        if giga_reply.image:
            image = BufferedInputFile(giga_reply.image, filename="giga.jpg")
            await message.reply_photo(image)
            return
        await message.reply(giga_reply.text_reply)


async def start_bot():
    if config.ENV == "prod":
        scheduler = AsyncIOScheduler()
        scheduler.add_job(send_photo_periodically, "interval", minutes=int(config.SEND_PHOTO_INTERVAL))
        scheduler.add_job(parse, "interval", hours=int(config.PARSE_INTERVAL))
        scheduler.start()

    await bot.set_my_commands(bot_commands)

    loop = asyncio.get_event_loop()
    loop.create_task(dp.start_polling(bot))
