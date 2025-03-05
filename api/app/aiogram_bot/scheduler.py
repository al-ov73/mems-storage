from aiogram import Bot
from aiogram.types import URLInputFile

from .models import Remainder
from .tasks import send_reminder
from ..config.config import PARSE_INTERVAL, SEND_PHOTO_INTERVAL, CHAT_ID, scheduler, timezone, tiny_db, bot
from ..config.dependencies import meme_repo
from ..config.db_config import db
from ..utils.parse import parse

from tinydb import Query


week_days = {
    "ПН": 0,
    "ВТ": 1,
    "СР": 2,
    "ЧТ": 3,
    "ПТ": 4,
    "СБ": 5,
    "ВС": 6,
}


def add_task(data: dict, bot: Bot) -> str:
    match data["type"]:
        case "dayly":
            job = add_daily_task(data, bot)
        case "weekly":
            job = add_weekly_task(data, bot)
        case "monthly":
            job = add_monthly_task(data, bot)
        case _:
            pass
    return job.id


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
                tiny_db.remove(Task.task_id == task_id)


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
        if j.name == "reminder":
            data = j.args[1]
            scheduled.append(Remainder(**data))
    return scheduled

async def send_photo_periodically():
    random_image = await meme_repo.get_random_meme(db=db)
    await bot.send_photo(CHAT_ID, URLInputFile(random_image.link))
    await meme_repo.make_meme_published(random_image.id, db)

def add_send_tasks() -> None:
    scheduler.add_job(send_photo_periodically, "interval", minutes=SEND_PHOTO_INTERVAL, name="parser")
    
def add_parse_tasks() -> None:
    scheduler.add_job(parse, "interval", hours=PARSE_INTERVAL, name="parser")