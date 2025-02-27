import os

from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import URLInputFile, Message

from ...config.config import (
    CHAT_ID,
    MY_API_ID,
    SEND_PHOTO_INTERVAL,
    STATIC_DIR,
    bot,
)
from ...config.db_config import db
from ...config.dependencies import meme_repo, visit_repo
from ...utils.os_utils import get_folder_size
from ...utils.parse import parse
from ...utils.stat_utils import format_memes_day_stat, format_visits_day_stat

memovoz_router = Router()


async def send_photo_periodically(type: str):
    random_image = await meme_repo.get_random_meme(db=db)
    await bot.send_photo(CHAT_ID, URLInputFile(random_image.link))
    await meme_repo.make_meme_published(random_image.id, db)


@memovoz_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {message.from_user.full_name}!")


@memovoz_router.message(Command(commands=["parse"]))
async def parse_command(message: Message):
    count_before = len(os.listdir(path=f"{STATIC_DIR}/photos"))
    folder_size_before = get_folder_size(f"{STATIC_DIR}/photos")
    reply = await bot.send_message(MY_API_ID, "Скачиваем картинки")
    await parse()
    count_after = len(os.listdir(path=f"{STATIC_DIR}/photos"))
    folder_size_after = get_folder_size(f"{STATIC_DIR}/photos")
    await bot.edit_message_text(
        text=f"Общий объем директории с мемами: {folder_size_before}МБ -> {folder_size_after}МБ\nСкачалось картинок: {count_after - count_before} ({count_before}->{count_after})",
        chat_id=reply.chat.id,
        message_id=reply.message_id,
    )


@memovoz_router.message(Command(commands=["send"]))
async def image_send_command(message: Message):
    await send_photo_periodically()
    await message.answer("Мем отправлен")


@memovoz_router.message(Command(commands=["stat"]))
async def stat_command(message: Message):
    day_stat = await meme_repo.get_published_stat(db=db)
    folder_size = get_folder_size(f"{STATIC_DIR}/photos")
    days_remain = day_stat.not_published / 24
    day_stats = await meme_repo.get_memes_count_by_day(db=db)
    formated_day_stat = await format_memes_day_stat(day_stats)
    await bot.send_message(
        MY_API_ID,
        f"Всего картинок: {day_stat.total} шт.\n"
        f"Опубликовано картинок: {day_stat.published} шт.\n"
        f"Не опубликовано: {day_stat.not_published} шт. ({round(days_remain)} дн.)\n"
        f"Отправляются каждые {SEND_PHOTO_INTERVAL / 60} ч.\n"
        f"Ожидают проверки: {day_stat.not_checked} шт. <a href='https://memovoz.ru/temp'>Проверить</a>\n"
        f"Общий объем мемов: {folder_size}МБ\n\n"
        f"{formated_day_stat}",
    )


@memovoz_router.message(Command(commands=["visits"]))
async def visits_command(message: Message):
    visits_stat = await visit_repo.get_visit_count_by_day(db=db)
    formated_day_stat = await format_visits_day_stat(visits_stat)
    old_visits = await visit_repo.get_old_users(db=db)
    await bot.send_message(
        MY_API_ID,
        f"Статистика визитов:\n" f"{formated_day_stat}\n" f"Всего старых пользователей: {old_visits}",
    )


@memovoz_router.message(Command(commands=["sources"]))
async def sources_command(message: Message):
    days_limit = 5
    total_count = 0
    sources_stat = await meme_repo.get_sources_stat(db=db, limit=days_limit)

    formated_stat = []
    for stat in sources_stat:
        day_stat = f"({stat.source_type}) {stat.source_name} - {stat.count} шт.\n"
        formated_stat.append(day_stat)
        total_count += stat.count

    day_average_count = round(total_count / days_limit, 2)
    await message.reply(
        f"Статистика за последние {days_limit} дн.\n"
        f"Среднее за день: {day_average_count}\n"
        f"{''.join(formated_stat)}"
    )


async def delete_last_message(chat_id: int | str, state: FSMContext):
    data = await state.get_data()
    last_message_id = data.get("last_message_id")

    if last_message_id:
        try:
            await bot.delete_message(chat_id=chat_id, message_id=last_message_id)
        except Exception as e:
            print(f"Не удалось удалить сообщение: {e}")
