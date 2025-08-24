import os
import time
from datetime import datetime, timedelta

from aiogram import Bot
from aiogram.types import URLInputFile
from apscheduler.triggers.interval import IntervalTrigger
from tinydb import Query

from ..config.config import (
    CHAT_ID,
    PARSE_INTERVAL,
    PHOTOS_DIR,
    PREVIEWS_DIR,
    SEND_PHOTO_INTERVAL,
    bot,
    months,
    scheduler,
    timezone,
    tiny_db,
)
from ..config.db_config import db
from ..config.dependencies import meme_repo, storage_repo, visit_repo
from ..config.logger_config import get_logger
from ..schemas.stat import StatSchema
from ..utils.parse import parse
from ..utils.stat_utils import format_visits_day_stat
from .models import Remainder
from .tasks import send_day_stat, send_reminder

logger = get_logger(__name__)

week_days = {
    "ПН": 0,
    "ВТ": 1,
    "СР": 2,
    "ЧТ": 3,
    "ПТ": 4,
    "СБ": 5,
    "ВС": 6,
}


def add_daily_task(data: dict, bot: Bot):
    return scheduler.add_job(
        send_reminder,
        "cron",
        name="reminder",
        hour=data["hour"],
        minute=data["minutes"],
        timezone=timezone,
        args=(bot, data),
    )


def add_weekly_task(data: dict, bot: Bot):
    return scheduler.add_job(
        send_reminder,
        "cron",
        name="reminder",
        day_of_week=week_days.get(data["week_day"]),
        hour=data["hour"],
        minute=data["minutes"],
        timezone=timezone,
        args=(bot, data),
    )


def get_week_parity() -> bool:
    return datetime.now().isocalendar()[1] % 2 == 0


def calculate_start_date(data: dict) -> datetime:
    """
    Вычисляет правильную дату старта с учётом:
    - Требуемой чётности недели
    - Указанного дня недели и времени
    - Текущей даты и времени
    """
    required_parity = data["is_even"]
    now = datetime.now()

    target_date = now.replace(hour=int(data["hour"]), minute=int(data["minutes"]), second=0, microsecond=0)

    target_weekday = week_days[data["week_day"]]

    days_ahead = (target_weekday - now.weekday() + 7) % 7
    target_date += timedelta(days=days_ahead)

    if target_date < now:
        target_date += timedelta(weeks=1)

    target_week_parity = target_date.isocalendar()[1] % 2 == 0
    if target_week_parity != required_parity:
        target_date += timedelta(weeks=1)

    return target_date


def add_two_weeks_task(data: dict, bot: Bot):
    start_date = calculate_start_date(data)

    return scheduler.add_job(
        send_reminder,
        trigger=IntervalTrigger(weeks=2, start_date=start_date, timezone=timezone),
        name="reminder",
        args=(bot, data),
    )


def add_monthly_task(data: dict, bot: Bot):
    return scheduler.add_job(
        send_reminder,
        "cron",
        name="reminder",
        day=data["month_day"],
        hour=data["hour"],
        minute=data["minutes"],
        timezone=timezone,
        args=(bot, data),
    )


def add_one_time_task(data: dict, bot: Bot):
    now = datetime.now()
    current_year = now.year
    target_date = datetime(
        year=current_year,
        month=months.get(data["month"]),
        day=int(data["month_day"]),
        hour=int(data["hour"]),
        minute=int(data["minutes"]),
    )

    if target_date < now:
        target_date = target_date.replace(year=current_year + 1)

    return scheduler.add_job(
        send_reminder,
        "date",
        name="reminder",
        run_date=target_date,
        timezone=timezone,
        args=(bot, data),
    )


def add_task(data: dict, bot: Bot) -> str:
    match data["type"]:
        case "one_time":
            job = add_one_time_task(data, bot)
        case "daily":
            job = add_daily_task(data, bot)
        case "weekly":
            job = add_weekly_task(data, bot)
        case "two_weeks":
            job = add_two_weeks_task(data, bot)
        case "monthly":
            job = add_monthly_task(data, bot)
        case _:
            raise Exception("Неверный тип напоминания")
    return job.id


def add_tasks_from_db(bot: Bot):
    jobs = tiny_db.all()
    for job in jobs:
        old_task_id = job["task_id"]
        new_task_id = add_task(job, bot)
        Task = Query()
        tiny_db.update({"task_id": new_task_id}, Task.task_id == old_task_id)


def rm_all_tasks_from_db():
    for j in scheduler.get_jobs():
        j.remove()


def delete_task(task_id: str) -> None:
    for j in scheduler.get_jobs():
        if j.name == "reminder":
            data = j.args[1]
            if data["task_id"] == task_id:
                scheduler.remove_job(j.id)
                Task = Query()
                tiny_db.remove(Task.task_id == j.id)


def get_formatted_task(task_id: str) -> str | None:
    for j in scheduler.get_jobs():
        if j.name == "reminder":
            data = j.args[1]
            if data["task_id"] == task_id:
                return str(Remainder(**data))
    return None


def get_reminders() -> list[Remainder]:
    scheduled = []
    for j in scheduler.get_jobs():
        print(j)
        if j.name == "reminder":
            data = j.args[1]
            scheduled.append(Remainder(**data))
    return scheduled


def get_next_call_of_remainders() -> list[Remainder]:
    scheduled = []
    for j in scheduler.get_jobs():
        name = j.args[1]["text"] if j.name == "reminder" else j.name
        scheduled.append(f"{name} - {j.next_run_time.strftime('%Y-%m-%d %H:%M')}")
    return scheduled


async def send_photo_periodically():
    random_image = await meme_repo.get_random_meme(db=db)
    await bot.send_photo(CHAT_ID, URLInputFile(random_image.link))
    await meme_repo.make_meme_published(random_image.id, db)


def add_send_tasks() -> None:
    scheduler.add_job(send_photo_periodically, "interval", name="send_photo_periodically", minutes=SEND_PHOTO_INTERVAL)


def add_parse_tasks() -> None:
    scheduler.add_job(parse, "interval", name="parse_periodically", hours=PARSE_INTERVAL)


async def clean_old_memes_task() -> None:
    await clean_old_memes()
    scheduler.add_job(clean_old_memes, "interval", name="clean_old_memes_periodically", hours=12)


async def clean_old_memes() -> None:
    logger.info("Clean_old_memes started")
    old_memes_names = await meme_repo.delete_old_memes(db=db)
    for name in old_memes_names:
        await storage_repo.delete_image(name)
    logger.info(f"Deleted {len(old_memes_names)} memes")


async def remove_not_used_files_task() -> None:
    await remove_not_used_files()
    scheduler.add_job(remove_not_used_files, "interval", name="remove_not_used_files", hours=12)


async def remove_not_used_files() -> None:
    logger.info("remove_not_used_files started")

    db_start = time.perf_counter()
    db_memes_names = await meme_repo.get_meme_names(db=db)
    db_time = time.perf_counter() - db_start
    logger.info(f"Fetched {len(db_memes_names)} meme names from DB in {db_time:.4f} seconds")

    memes_delete_count = 0
    photos_start = time.perf_counter()
    with os.scandir(PHOTOS_DIR) as entries:
        for entry in entries:
            if entry.name not in db_memes_names:
                storage_repo.delete_image(entry.name)
                memes_delete_count += 1
    photos_time = time.perf_counter() - photos_start
    logger.info(f"Deleted {memes_delete_count} files from {PHOTOS_DIR} in {photos_time:.4f} seconds")

    previews_delete_count = 0
    previews_start = time.perf_counter()
    with os.scandir(PREVIEWS_DIR) as entries:
        for entry in entries:
            if entry.name not in db_memes_names:
                storage_repo.delete_image(entry.name)
                previews_delete_count += 1
    previews_time = time.perf_counter() - previews_start
    logger.info(f"Deleted {previews_delete_count} previews from {PREVIEWS_DIR} in {previews_time:.4f} seconds")


async def send_photo_periodically():
    random_image = await meme_repo.get_random_meme(db=db)
    await bot.send_photo(CHAT_ID, URLInputFile(random_image.link))
    await meme_repo.make_meme_published(random_image.id, db)


async def send_daystat_every_day():
    day_stat: StatSchema = await meme_repo.get_published_stat(db=db)
    days_remain = day_stat.not_published / 24
    visits_stat = await visit_repo.get_visit_count_by_day(db=db, limit=2)
    formatted_visits_stat = format_visits_day_stat(visits_stat)
    weekly_visit_stat = await visit_repo.get_weekly_visits_stats(db=db)
    monthly_visit_stat = await visit_repo.get_monthly_visits_stats(db=db)
    formatted_day_stat = (
        f"Статистика за {datetime.now().strftime('%d-%m-%Y')}\n"
        f"Всего картинок: {day_stat.total} шт.\n"
        f"Опубликовано картинок: {day_stat.published} шт.\n"
        f"Не опубликовано: {day_stat.not_published} шт. ({round(days_remain)} дн.)\n"
        f"Ожидают проверки: {day_stat.not_checked} шт.\n\n"
        f"Статистика визитов:\n"
        f"{formatted_visits_stat}\n\n{weekly_visit_stat}\n\n{monthly_visit_stat}"
    )

    scheduler.add_job(
        send_day_stat,
        name="send_day_stat",
        trigger="cron",
        hour=9,
        minute=30,
        timezone=timezone,
        args=(bot, formatted_day_stat),
    )
