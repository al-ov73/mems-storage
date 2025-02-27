from aiogram import Dispatcher
from aiogram.exceptions import TelegramConflictError
from filelock import FileLock, Timeout

from .commands import bot_commands
from .routers.gigachat import gigachat_router
from .routers.memovoz import send_photo_periodically, memovoz_router
from .routers.reminder import reminder_router
from .scheduler import (
    add_tasks_from_db,
)
from ..config.config import (
    ENV,
    PARSE_INTERVAL,
    SEND_PHOTO_INTERVAL,
    scheduler,
    bot,
)
from ..utils.parse import parse

dp = Dispatcher()
dp.include_router(memovoz_router)
dp.include_router(reminder_router)
dp.include_router(gigachat_router)
LOCK_FILE = "/tmp/bot.lock"  # Путь к файлу блокировки


async def start_bot():
    lock = FileLock(
        LOCK_FILE
    )  # Использование файловой блокировки для предотвращения запуска нескольких экземпляров бота

    try:
        # Попытка захватить блокировку
        with lock.acquire(timeout=5):  # Устанавливаем таймаут для ожидания блокировки
            ENV = "prod"
            if ENV == "prod":
                add_tasks_from_db(bot)
                scheduler.add_job(send_photo_periodically, "interval", minutes=SEND_PHOTO_INTERVAL, args=("parser",))
                scheduler.add_job(parse, "interval", hours=PARSE_INTERVAL, args=("parser",))
                scheduler.start()

            await bot.set_my_commands(bot_commands)

            try:
                print("Запуск бота...")
                await dp.start_polling(bot)
            except TelegramConflictError:
                print("Ошибка: Бот уже запущен в другом месте!")
            except Exception as e:
                print(f"Произошла ошибка: {e}")
            finally:
                print("Бот остановлен.")
    except Timeout:
        print("Не удалось захватить блокировку. Другой процесс уже запустил бота.")
