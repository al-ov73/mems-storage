from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from ..config.config import remainder_types, scheduler

from .models import Remainder


def confirm_keyboard(prefix: str, task_id: str = None):
    builder = InlineKeyboardBuilder()
    builder.button(text="Да", callback_data=f"{prefix}__Да__{task_id}")
    builder.button(text="Нет", callback_data=f"{prefix}__Нет")
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

def delete_task_keyboard():
    builder = InlineKeyboardBuilder()

    for j in scheduler.get_jobs():
        data = j.args[1]
        remainder = Remainder(**data)
        builder.button(text=str(remainder), callback_data=f"task__{remainder.task_id}")
    builder.button(text="Отменить", callback_data=f"task__")
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)

def type_keyboard():
    builder = ReplyKeyboardBuilder()
    for value in remainder_types:
        builder.button(text=value)
    builder.adjust(3)
    return builder.as_markup(resize_keyboard=True)

def week_day_keyboard():
    builder = ReplyKeyboardBuilder()
    days = ["ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ", "ВС"]
    for day in days:
        builder.button(text=day)
    builder.adjust(3)
    return builder.as_markup(resize_keyboard=True)

def hour_keyboard():
    builder = ReplyKeyboardBuilder()
    for hour in range(0, 24):
        builder.button(text=str(hour))
    builder.adjust(6)
    return builder.as_markup(resize_keyboard=True)

def month_day_keyboard():
    builder = ReplyKeyboardBuilder()
    for hour in range(1, 32):
        builder.button(text=str(hour))
    builder.adjust(6)
    return builder.as_markup(resize_keyboard=True)

def minutes_keyboard():
    builder = ReplyKeyboardBuilder()
    for minute in ["00", "15", "30", "45"]:
        builder.button(text=minute)
    builder.adjust(4)
    return builder.as_markup(resize_keyboard=True)

keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="📝Статистика", callback_data="stat"),
            InlineKeyboardButton(text="📝Статистика визитов", callback_data="visits"),
            InlineKeyboardButton(text="‼️Парсить‼️", callback_data="parse"),
            InlineKeyboardButton(text="👥Отпр. мем", callback_data="send"),
        ]
    ],
)
