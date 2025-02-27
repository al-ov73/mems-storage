import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import URLInputFile, Message, BufferedInputFile, ErrorEvent
from aiogram.exceptions import TelegramConflictError
from aiogram.utils.chat_action import ChatActionSender
from aiogram.types import ReplyKeyboardRemove

from filelock import FileLock, Timeout

from .keyboards import confirm_keyboard, delete_task_keyboard, hour_keyboard, minutes_keyboard, month_day_keyboard, type_keyboard, week_day_keyboard
from .scheduler import add_task, delete_task, get_formatted_jobs, get_formatted_task, rm_all_tasks_from_db
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from .commands import bot_commands
from ..config.config import CHAT_ID, ENV, MY_API_ID, PARSE_INTERVAL, SEND_PHOTO_INTERVAL, STATIC_DIR, tiny_db, BOT_TOKEN
from ..config.db_config import db
from ..config.dependencies import meme_repo, visit_repo
from ..utils.gigachat import get_response_from_gigachat
from ..utils.os_utils import get_folder_size
from ..utils.stat_utils import format_memes_day_stat, format_visits_day_stat
from ..utils.parse import parse
from ..config.config import remainder_types

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
LOCK_FILE = "/tmp/bot.lock"  # Путь к файлу блокировки


async def send_photo_periodically():
    random_image = await meme_repo.get_random_meme(db=db)
    await bot.send_photo(CHAT_ID, URLInputFile(random_image.link))
    await meme_repo.make_meme_published(random_image.id, db)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {message.from_user.full_name}!")


@dp.message(Command(commands=["parse"]))
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


@dp.message(Command(commands=["send"]))
async def image_send_command(message: Message):
    await send_photo_periodically()
    await message.answer("Мем отправлен")


@dp.message(Command(commands=["stat"]))
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


@dp.message(Command(commands=["visits"]))
async def visits_command(message: Message):
    visits_stat = await visit_repo.get_visit_count_by_day(db=db)
    formated_day_stat = await format_visits_day_stat(visits_stat)
    old_visits = await visit_repo.get_old_users(db=db)
    await bot.send_message(
        MY_API_ID,
        f"Статистика визитов:\n" f"{formated_day_stat}\n" f"Всего старых пользователей: {old_visits}",
    )


@dp.message(Command(commands=["sources"]))
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


class Remainder(StatesGroup):
    type = State()
    month_day = State()
    week_day = State()
    hour = State()
    minutes = State()
    confirm = State()
    text = State()
    last_message_id = State()

@dp.message(Command("add_reminder"))
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer("Введи тип напоминания:", reply_markup=type_keyboard())
    await state.set_state(Remainder.type)

@dp.message(Remainder.type)
async def process_name(message: types.Message, state: FSMContext):
    await delete_last_message(message.chat.id, state)
    reminder_type = remainder_types.get(message.text)
    
    if not reminder_type:
        await message.answer("Неизвестный тип напоминания. Попробуйте снова.")
        return

    await state.update_data(type=reminder_type)

    actions = {
        "dayly": {
            "update": {"month_day": "", "week_day": ""},
            "message": "Введите часы:",
            "keyboard": hour_keyboard(),
            "next_state": Remainder.hour
        },
        "weekly": {
            "update": {"month_day": ""},
            "message": "В какой день недели делать напоминание?",
            "keyboard": week_day_keyboard(),
            "next_state": Remainder.week_day
        },
        "monthly": {
            "update": {"week_day": ""},
            "message": "Какого числа делать напоминание?",
            "keyboard": month_day_keyboard(),
            "next_state": Remainder.month_day
        }
    }

    action = actions.get(reminder_type)
    if action:
        await state.update_data(**action["update"])
        sent_message = await message.answer(action["message"], reply_markup=action["keyboard"])
        await state.update_data(last_message_id=sent_message.message_id)
        await state.set_state(action["next_state"])
    else:
        await message.answer("Неизвестный тип напоминания. Попробуйте снова.")

@dp.message(Remainder.week_day)
async def process_name(message: types.Message, state: FSMContext):
    await delete_last_message(message.chat.id, state)
    await state.update_data(week_day=message.text)
    sent_message = await message.answer(f"Введите часы:", reply_markup=hour_keyboard())
    await state.update_data(last_message_id=sent_message.message_id)
    await state.set_state(Remainder.hour)

@dp.message(Remainder.month_day)
async def process_name(message: types.Message, state: FSMContext):
    await delete_last_message(message.chat.id, state)
    await state.update_data(month_day=message.text)
    sent_message = await message.answer(f"Введите часы:", reply_markup=hour_keyboard())
    await state.update_data(last_message_id=sent_message.message_id)
    await state.set_state(Remainder.hour)
    
@dp.message(Remainder.hour)
async def process_name(message: types.Message, state: FSMContext):
    await delete_last_message(message.chat.id, state)
    await state.update_data(hour=message.text)
    sent_message = await message.answer(f"Введите минуты:", reply_markup=minutes_keyboard())
    await state.update_data(last_message_id=sent_message.message_id)
    await state.set_state(Remainder.minutes)

@dp.message(Remainder.minutes)
async def process_name(message: types.Message, state: FSMContext):
    await delete_last_message(message.chat.id, state)
    await state.update_data(minutes=message.text)
    sent_message = await message.answer(f"Введите текст напоминания:", reply_markup=ReplyKeyboardRemove())
    await state.update_data(last_message_id=sent_message.message_id)
    await state.set_state(Remainder.text)

@dp.message(Remainder.text)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(text=message.text)
    data = await state.get_data()
    del data["last_message_id"]
    data["user_id"] = message.from_user.id
    data["task_id"] = add_task(data, bot)
    tiny_db.insert(data)
    sent_message = await message.answer("Уведомление добавлено", reply_markup=ReplyKeyboardRemove())
    await state.update_data(last_message_id=sent_message.message_id)
    await state.clear()

@dp.message(Command("reminders"))
async def cmd_start(message: types.Message, state: FSMContext):
    await delete_last_message(message.chat.id, state)
    formated_reminders = get_formatted_jobs()
    sent_message = await message.answer(f"текущие напоминания:\n\n{formated_reminders}")
    await state.update_data(last_message_id=sent_message.message_id)

@dp.message(Command("purge"))
async def cmd_start(message: types.Message, state: FSMContext):
    await delete_last_message(message.chat.id, state)
    sent_message = await message.answer(
            text="Вы уверены, что хотите удалить ВСЕ напоминания???",
            reply_markup=confirm_keyboard("task_purge"),
        )
    await state.update_data(last_message_id=sent_message.message_id)

    
@dp.message(Command("delete"))
async def cmd_start(message: types.Message, state: FSMContext):
    await delete_last_message(message.chat.id, state)
    sent_message = await message.answer(f"Какое напоминание удалить?", reply_markup=delete_task_keyboard())
    await state.update_data(last_message_id=sent_message.message_id)

@dp.callback_query(lambda c: c.data.startswith("task_purge__"))
async def handle_task_selection(callback: types.CallbackQuery, state: FSMContext):
    await delete_last_message(callback.message.chat.id, state)
    should_purge = callback.data.split("__")[1]
    if should_purge == "Да":
        db.truncate()
        rm_all_tasks_from_db()
        sent_message = await bot.send_message(callback.from_user.id, "Все напоминания удалены", reply_markup=ReplyKeyboardRemove())
        await state.update_data(last_message_id=sent_message.message_id)
    else:
        await bot.send_message(callback.from_user.id, "Отмена", reply_markup=ReplyKeyboardRemove())
    
@dp.callback_query(lambda c: c.data.startswith("task__"))
async def handle_task_selection(callback: types.CallbackQuery, state: FSMContext):
    await delete_last_message(callback.message.chat.id, state)
    task_id = callback.data.split("__")[1]
    if task_id:
        task = get_formatted_task(task_id)
        sent_message = await bot.send_message(
            callback.from_user.id,
            text=f"Хотите удалить уведомление\n{task}",
            reply_markup=confirm_keyboard("task_delete", task_id),
        )
        await state.update_data(last_message_id=sent_message.message_id)
    else:
        await bot.send_message(callback.from_user.id, "Отмена", reply_markup=ReplyKeyboardRemove())

@dp.callback_query(lambda c: c.data.startswith("task_delete__"))
async def handle_task_selection(callback: types.CallbackQuery, state: FSMContext):
    await delete_last_message(callback.message.chat.id, state)
    should_delete = callback.data.split("__")[1]
    if should_delete == "Да":
        task_id = callback.data.split("__")[2]
        delete_task(task_id)
        sent_message = await bot.send_message(callback.from_user.id, f"Напоминание удалено", reply_markup=ReplyKeyboardRemove())
        await state.update_data(last_message_id=sent_message.message_id)
    else:
        sent_message = await bot.send_message(callback.from_user.id, "Отмена", reply_markup=ReplyKeyboardRemove())
        await state.update_data(last_message_id=sent_message.message_id)


async def start_bot():
    # Использование файловой блокировки для предотвращения запуска нескольких экземпляров бота
    lock = FileLock(LOCK_FILE)

    try:
        # Попытка захватить блокировку
        with lock.acquire(timeout=5):  # Устанавливаем таймаут для ожидания блокировки
            if ENV == "prod":
                scheduler = AsyncIOScheduler()
                scheduler.add_job(
                    send_photo_periodically,
                    "interval",
                    minutes=SEND_PHOTO_INTERVAL,
                )
                scheduler.add_job(parse, "interval", hours=PARSE_INTERVAL)
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


@dp.message()
async def other_command(message: Message) -> None:
    giga_reply = await get_response_from_gigachat(message.text)
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        if giga_reply.image:
            image = BufferedInputFile(giga_reply.image, filename="giga.jpg")
            await message.reply_photo(image)
            return
        await message.reply(giga_reply.text_reply)