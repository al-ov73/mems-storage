from datetime import datetime, timedelta
from aiogram import Bot
from aiogram.types import URLInputFile

from ..utils.stat_utils import format_visits_day_stat
from ..schemas.stat import StatSchema
from .models import Remainder
from .tasks import send_day_stat, send_reminder
from ..config.config import PARSE_INTERVAL, SEND_PHOTO_INTERVAL, CHAT_ID, scheduler, timezone, tiny_db, bot
from ..config.dependencies import meme_repo, visit_repo
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
week_days = {
    "monday": "mon",
    "tuesday": "tue",
    "wednesday": "wed",
    "thursday": "thu",
    "friday": "fri",
    "saturday": "sat",
    "sunday": "sun"
}

def get_week_parity() -> bool:
    """Возвращает True для чётной недели, False для нечётной."""
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
    
    # Создаем целевую дату с правильным временем
    target_time = datetime.strptime(data["time"], "%H:%M").time()
    target_date = now.replace(
        hour=target_time.hour,
        minute=target_time.minute,
        second=0,
        microsecond=0
    )
    
    # Получаем числовое представление дня недели (0-пн, 6-вс)
    target_weekday = list(week_days.values()).index(data["week_day"])
    
    # Корректируем день недели
    days_ahead = (target_weekday - now.weekday() + 7) % 7
    target_date += timedelta(days=days_ahead)
    
    # Если время уже прошло на этой неделе, переносим на следующую неделю
    if target_date < now:
        target_date += timedelta(weeks=1)
    
    # Проверяем четность недели у полученной даты
    target_week_parity = target_date.isocalendar()[1] % 2 == 0
    
    # Корректируем по четности
    if target_week_parity != required_parity:
        target_date += timedelta(weeks=1)
    
    return target_date

def add_two_weeks_task(data: dict, bot: Bot):
    start_date = calculate_start_date(data)
    
    return scheduler.add_job(
        send_reminder,
        "cron",
        name="reminder",
        start_date=start_date,
        day_of_week=data["week_day"],  # например "mon", "tue"
        week="*/2",  # выполнять каждые 2 недели
        hour=data["hour"],
        minute=data["minutes"],
        timezone=data.get("timezone", "UTC"),
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

task_handlers = {
    "daily": add_daily_task,
    "weekly": add_weekly_task,
    "two_weeks": add_two_weeks_task,
    "monthly": add_monthly_task,
}

def add_task(data: dict, bot: Bot) -> str:
    match data["type"]:
        case "daily":
            job = add_daily_task(data, bot)
        case "weekly":
            job = add_weekly_task(data, bot)
        case "two_weeks":
            job = add_two_weeks_task(data, bot)
        case "monthly":
            job = add_monthly_task(data, bot)
        case _:
            pass
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
        scheduled.append(f"{name} - {j.next_run_time.strftime("%Y-%m-%d %H:%M")}")
    return scheduled

async def send_photo_periodically():
    random_image = await meme_repo.get_random_meme(db=db)
    await bot.send_photo(CHAT_ID, URLInputFile(random_image.link))
    await meme_repo.make_meme_published(random_image.id, db)

def add_send_tasks() -> None:
    scheduler.add_job(send_photo_periodically, "interval", name="send_photo_periodically", minutes=SEND_PHOTO_INTERVAL)
    
def add_parse_tasks() -> None:
    scheduler.add_job(parse, "interval", name="parse_periodically",  hours=PARSE_INTERVAL)
    
async def send_photo_periodically():
    random_image = await meme_repo.get_random_meme(db=db)
    await bot.send_photo(CHAT_ID, URLInputFile(random_image.link))
    await meme_repo.make_meme_published(random_image.id, db)
    
async def send_daystat_every_day():
    day_stat: StatSchema = await meme_repo.get_published_stat(db=db)
    days_remain = day_stat.not_published / 24
    visits_stat = await visit_repo.get_visit_count_by_day(db=db, limit = 2)
    formatted_visits_stat = format_visits_day_stat(visits_stat)
    formatted_day_stat = (
        f"Статистика за {datetime.now().strftime('%d-%m-%Y')}\n"
        f"Всего картинок: {day_stat.total} шт.\n"
        f"Опубликовано картинок: {day_stat.published} шт.\n"
        f"Не опубликовано: {day_stat.not_published} шт. ({round(days_remain)} дн.)\n"
        f"Ожидают проверки: {day_stat.not_checked} шт.\n\n"
        f"Статистика визитов:\n"
        f"{formatted_visits_stat}")

    scheduler.add_job(
        send_day_stat,
        name="send_day_stat",
        trigger="cron",
        hour=9,
        minute=30,
        timezone=timezone,
        args=(bot, formatted_day_stat),
    )
