import os

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import Message

from ...config.config import SEND_PHOTO_INTERVAL, STATIC_DIR
from ...config.db_config import db
from ...config.dependencies import meme_repo, visit_repo
from ...utils.os_utils import get_folder_size
from ...utils.parse import parse
from ...utils.stat_utils import format_memes_day_stat, format_visits_day_stat
from ..commands import TelegramCommands
from ..keyboards import memovoz_mng_keyboard, notchecked_keyboard

memovoz_router = Router()


@memovoz_router.message(Command(commands=[TelegramCommands.MEMOVOZ.value.name]))
async def command_start_handler(message: Message) -> None:
    await message.answer("Управление сайтом memovoz.ru:", reply_markup=memovoz_mng_keyboard())


@memovoz_router.callback_query(lambda c: c.data == "parse")
async def parse_callback(callback_query: types.CallbackQuery):
    count_before = len(os.listdir(path=f"{STATIC_DIR}/photos"))
    folder_size_before = get_folder_size(f"{STATIC_DIR}/photos")
    reply = await callback_query.message.answer("Скачиваем картинки")
    await parse()
    count_after = len(os.listdir(path=f"{STATIC_DIR}/photos"))
    folder_size_after = get_folder_size(f"{STATIC_DIR}/photos")
    await callback_query.message.edit_text(
        text=f"Общий объем директории с мемами: {folder_size_before}МБ -> {folder_size_after}МБ\nСкачалось картинок: {count_after - count_before} ({count_before}->{count_after})",
    )


@memovoz_router.callback_query(lambda c: c.data == "stat")
async def stat_command(callback_query: types.CallbackQuery):
    day_stat = await meme_repo.get_published_stat(db=db)
    folder_size = get_folder_size(f"{STATIC_DIR}/photos")
    days_remain = day_stat.not_published / 24
    day_stats = await meme_repo.get_memes_count_by_day(db=db)
    formated_day_stat = await format_memes_day_stat(day_stats)
    await callback_query.message.answer(
        f"Всего картинок: {day_stat.total} шт.\n"
        f"Опубликовано картинок: {day_stat.published} шт.\n"
        f"Не опубликовано: {day_stat.not_published} шт. ({round(days_remain)} дн.)\n"
        f"Отправляются каждые {SEND_PHOTO_INTERVAL / 60} ч.\n"
        f"Ожидают проверки: {day_stat.not_checked} шт.\n"
        f"Общий объем мемов: {folder_size}МБ\n\n"
        f"{formated_day_stat}",
        reply_markup=notchecked_keyboard(day_stat.not_checked),
    )


@memovoz_router.callback_query(lambda c: c.data == "visits")
async def visits_callback(callback_query: types.CallbackQuery):
    visits_stat = await visit_repo.get_visit_count_by_day(db=db)
    formated_day_stat = format_visits_day_stat(visits_stat)
    old_visits = await visit_repo.get_old_users(db=db)

    await callback_query.message.answer(
        f"Статистика визитов:\n" f"{formated_day_stat}\n" f"Всего старых пользователей: {old_visits}"
    )
    await callback_query.answer()


@memovoz_router.callback_query(lambda c: c.data == "sources")
async def sources_callback(callback_query: types.CallbackQuery):
    days_limit = 5
    total_count = 0
    sources_stat = await meme_repo.get_sources_stat(db=db, limit=days_limit)

    formated_stat = []
    for stat in sources_stat:
        day_stat = f"({stat.source_type}) {stat.source_name} - {stat.count} шт.\n"
        formated_stat.append(day_stat)
        total_count += stat.count

    day_average_count = round(total_count / days_limit, 2)

    await callback_query.message.answer(
        f"Статистика за последние {days_limit} дн.\n"
        f"Среднее за день: {day_average_count}\n"
        f"{''.join(formated_stat)}"
    )
    await callback_query.answer()
