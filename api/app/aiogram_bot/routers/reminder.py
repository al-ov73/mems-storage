from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, BufferedInputFile
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.chat_action import ChatActionSender
import datetime

from ..commands import TelegramCommands

from ..keyboards import (
    confirm_keyboard,
    delete_task_keyboard,
    hour_keyboard,
    is_even_keyboard,
    minutes_keyboard,
    month_day_keyboard,
    month_keyboard,
    reminders_mng_keyboard,
    type_keyboard,
    week_day_keyboard,
)
from ..scheduler import add_task, delete_task, get_next_call_of_remainders, get_reminders, get_formatted_task, get_week_parity, rm_all_tasks_from_db

from ...config.config import remainder_types
from ...config.config import tiny_db, bot

reminder_router = Router()

class Remainder(StatesGroup):
    type = State()
    is_even = State()
    month = State()
    month_day = State()
    week_day = State()
    hour = State()
    minutes = State()
    confirm = State()
    text = State()
    last_message_id = State()

async def delete_last_message(chat_id: int | str, state: FSMContext):
    data = await state.get_data()
    last_message_id = data.get("last_message_id")

    if last_message_id:
        try:
            await bot.delete_message(chat_id=chat_id, message_id=last_message_id)
        except Exception as e:
            print(f"Не удалось удалить сообщение: {e}")

@reminder_router.message(Command(commands=[TelegramCommands.REMINDERS.value.name]))
async def command_start_handler(message: Message) -> None:
    await message.answer("Управление напоминаниями:", reply_markup=reminders_mng_keyboard())

@reminder_router.callback_query(lambda c: c.data == "add_reminder")
async def add_reminder_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer("Введи тип напоминания:", reply_markup=type_keyboard())
    await state.set_state(Remainder.type)
    await callback_query.answer()

@reminder_router.callback_query(lambda c: c.data == "reminders")
async def reminders_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await delete_last_message(callback_query.message.chat.id, state)
    reminders = get_reminders()
    formated_reminders = "\n".join(str(r) for r in reminders)
    sent_message = await callback_query.message.answer(f"Текущие напоминания:\n\n{formated_reminders}")
    await state.update_data(last_message_id=sent_message.message_id)
    await callback_query.answer()

@reminder_router.callback_query(lambda c: c.data == "when_next")
async def reminders_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await delete_last_message(callback_query.message.chat.id, state)
    reminders = get_next_call_of_remainders()
    formated_reminders = "\n".join(reminders)
    sent_message = await callback_query.message.answer(f"Время следующего напоминания:\n\n{formated_reminders}")
    await state.update_data(last_message_id=sent_message.message_id)
    await callback_query.answer()
    
@reminder_router.callback_query(lambda c: c.data == "delete")
async def delete_reminder_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await delete_last_message(callback_query.message.chat.id, state)
    sent_message = await callback_query.message.answer("Какое напоминание удалить?", reply_markup=delete_task_keyboard())
    await state.update_data(last_message_id=sent_message.message_id)
    await callback_query.answer()

@reminder_router.callback_query(lambda c: c.data == "purge")
async def purge_reminders_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await delete_last_message(callback_query.message.chat.id, state)
    sent_message = await callback_query.message.answer(
        text="Вы уверены, что хотите удалить ВСЕ напоминания???",
        reply_markup=confirm_keyboard("task_purge"),
    )
    await state.update_data(last_message_id=sent_message.message_id)
    await callback_query.answer()
    
@reminder_router.message(Remainder.type)
async def process_type(message: types.Message, state: FSMContext):
    """
    process remainder type
    """
    await delete_last_message(message.chat.id, state)
    reminder_type = remainder_types.get(message.text)

    await state.update_data(
        week_day = "",
        is_even = "",
        month = "",
        month_day = ""
    )
    if not reminder_type:
        await message.answer("Неизвестный тип напоминания. Попробуйте снова.")
        return

    await state.update_data(type=reminder_type)
    parity = "четная" if get_week_parity() else "нечетная"
    actions = {
        "one_time": {
            "message": "Введите месяц:",
            "keyboard": month_keyboard(),
            "next_state": Remainder.month,
        },
        "daily": {
            "message": "Введите часы:",
            "keyboard": hour_keyboard(),
            "next_state": Remainder.hour,
        },
        "weekly": {
            "message": "В какой день недели делать напоминание?",
            "keyboard": week_day_keyboard(),
            "next_state": Remainder.week_day,
        },
        "two_weeks": {
            "message": f"На какой неделе сообщать? Сейчас {parity} неделя",
            "keyboard": is_even_keyboard(),
            "next_state": Remainder.is_even,
        },
        "monthly": {
            "message": "Какого числа делать напоминание?",
            "keyboard": month_day_keyboard(),
            "next_state": Remainder.month_day,
        },
    }

    action = actions.get(reminder_type)
    if action:
        sent_message = await message.answer(action["message"], reply_markup=action["keyboard"])
        await state.update_data(last_message_id=sent_message.message_id)
        await state.set_state(action["next_state"])
    else:
        await message.answer("Неизвестный тип напоминания. Попробуйте снова.")


@reminder_router.message(Remainder.is_even)
async def process_name(message: types.Message, state: FSMContext):
    """
    get is_even
    process week day
    """
    await delete_last_message(message.chat.id, state)
    await state.update_data(is_even=message.text)
    sent_message = await message.answer(f"В какой день недели делать напоминание?", reply_markup=week_day_keyboard())
    await state.update_data(last_message_id=sent_message.message_id)
    await state.set_state(Remainder.week_day)

@reminder_router.message(Remainder.week_day)
async def process_hour(message: types.Message, state: FSMContext):
    """
    get week day
    process hours
    """
    await delete_last_message(message.chat.id, state)
    await state.update_data(week_day=message.text)
    sent_message = await message.answer(f"Введите часы:", reply_markup=hour_keyboard())
    await state.update_data(last_message_id=sent_message.message_id)
    await state.set_state(Remainder.hour)

@reminder_router.message(Remainder.month)
async def process_name(message: types.Message, state: FSMContext):
    """
    get month
    process month_day 
    """
    await delete_last_message(message.chat.id, state)
    await state.update_data(month=message.text)
    sent_message = await message.answer(f"Какого числа делать напоминание?", reply_markup=month_day_keyboard())
    await state.update_data(last_message_id=sent_message.message_id)
    await state.set_state(Remainder.month_day)


@reminder_router.message(Remainder.month_day)
async def process_name(message: types.Message, state: FSMContext):
    """
    get month day
    process hours 
    """
    await delete_last_message(message.chat.id, state)
    await state.update_data(month_day=message.text)
    sent_message = await message.answer(f"Введите часы:", reply_markup=hour_keyboard())
    await state.update_data(last_message_id=sent_message.message_id)
    await state.set_state(Remainder.hour)


@reminder_router.message(Remainder.hour)
async def process_name(message: types.Message, state: FSMContext):
    """
    get hours
    process minutes
    """
    await delete_last_message(message.chat.id, state)
    await state.update_data(hour=message.text)
    sent_message = await message.answer(f"Введите минуты:", reply_markup=minutes_keyboard())
    await state.update_data(last_message_id=sent_message.message_id)
    await state.set_state(Remainder.minutes)


@reminder_router.message(Remainder.minutes)
async def process_name(message: types.Message, state: FSMContext):
    """
    get minutes
    process text
    """
    await delete_last_message(message.chat.id, state)
    await state.update_data(minutes=message.text)
    sent_message = await message.answer(f"Введите текст напоминания:", reply_markup=ReplyKeyboardRemove())
    await state.update_data(last_message_id=sent_message.message_id)
    await state.set_state(Remainder.text)


@reminder_router.message(Remainder.text)
async def process_name(message: types.Message, state: FSMContext):
    """
    get text
    add remainder to db and scheduler
    """
    await state.update_data(text=message.text)
    data = await state.get_data()
    del data["last_message_id"]
    data["is_even"] = True if data["is_even"] == "Четная" else False
    data["user_id"] = message.from_user.id
    data["task_id"] = add_task(data, bot)
    tiny_db.insert(data)
    sent_message = await message.answer("Уведомление добавлено", reply_markup=ReplyKeyboardRemove())
    await state.update_data(last_message_id=sent_message.message_id)
    await state.clear()

@reminder_router.callback_query(lambda c: c.data.startswith("task_purge__"))
async def handle_remainder_purge(callback: types.CallbackQuery, state: FSMContext):
    """
    purge remainder
    """
    await delete_last_message(callback.message.chat.id, state)
    should_purge = callback.data.split("__")[1]
    if should_purge == "Да":
        tiny_db.truncate()
        rm_all_tasks_from_db()
        sent_message = await bot.send_message(
            callback.from_user.id, "Все напоминания удалены", reply_markup=ReplyKeyboardRemove()
        )
        await state.update_data(last_message_id=sent_message.message_id)
    else:
        await bot.send_message(callback.from_user.id, "Отмена", reply_markup=ReplyKeyboardRemove())


@reminder_router.callback_query(lambda c: c.data.startswith("task__"))
async def handle_remainder_delete(callback: types.CallbackQuery, state: FSMContext):
    """
    delete remainder
    """
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


@reminder_router.callback_query(lambda c: c.data.startswith("task_delete__"))
async def handle_task_selection(callback: types.CallbackQuery, state: FSMContext):
    """
    delete remainder after confirmation
    """
    await delete_last_message(callback.message.chat.id, state)
    should_delete = callback.data.split("__")[1]
    if should_delete == "Да":
        task_id = callback.data.split("__")[2]
        delete_task(task_id)
        sent_message = await bot.send_message(
            callback.from_user.id, f"Напоминание удалено", reply_markup=ReplyKeyboardRemove()
        )
        await state.update_data(last_message_id=sent_message.message_id)
    else:
        sent_message = await bot.send_message(callback.from_user.id, "Отмена", reply_markup=ReplyKeyboardRemove())
        await state.update_data(last_message_id=sent_message.message_id)
