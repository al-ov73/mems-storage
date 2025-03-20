from aiogram import Dispatcher
from aiogram.exceptions import TelegramConflictError
from filelock import FileLock, Timeout

from .commands import bot_commands
from .routers.gigachat import gigachat_router
from .routers.memovoz import memovoz_router
from .routers.reminder import reminder_router
from .routers.vacancies.vacancies import vacancies_router
from .scheduler import (
    add_parse_tasks,
    add_send_tasks,
    add_tasks_from_db,
    send_daystat_every_day,
)
from ..config.config import (
    scheduler,
    bot,
)


dp = Dispatcher()
dp.include_router(memovoz_router)
dp.include_router(reminder_router)
dp.include_router(vacancies_router)
dp.include_router(gigachat_router)
LOCK_FILE = "/tmp/bot.lock"  # Путь к файлу блокировки

async def start_bot():
    # Использование файловой блокировки для предотвращения запуска нескольких экземпляров бота
    lock = FileLock(LOCK_FILE)
    try:
        with lock.acquire(timeout=5):  # таймаут для ожидания блокировки
            add_tasks_from_db(bot)
            add_send_tasks()
            add_parse_tasks()
            await send_daystat_every_day()
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
