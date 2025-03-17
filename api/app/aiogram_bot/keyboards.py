from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from .scheduler import get_reminders
from ..config.config import NOT_CHECKED_URL, remainder_types


# class TelegramCommand:
#                 [InlineKeyboardButton(text="Добавить", callback_data="add_reminder")],
#             [InlineKeyboardButton(text="Напоминания", callback_data="reminders")],
#             [InlineKeyboardButton(text="Удалить напоминание", callback_data="delete")],
#             [InlineKeyboardButton(text="Удалить все", callback_data="purge")],

# class RemainderCommands:
#     ADD_REMINDER = "add_reminder"
#     REMINDERS = "reminders"
#     DELETE = "delete"
#     PURGE = "purge"
#     MEMOVOZ = "memovoz"
#     STAT = "stat"
    


def notchecked_keyboard(notchecked_count: int) -> InlineKeyboardButton:
    builder = InlineKeyboardBuilder()
    builder.button(text=f"Проверить {notchecked_count} шт.", web_app=WebAppInfo(url=NOT_CHECKED_URL))
    return builder.as_markup(resize_keyboard=True)

def confirm_keyboard(prefix: str, task_id: str = None):
    builder = InlineKeyboardBuilder()
    builder.button(text="Да", callback_data=f"{prefix}__Да__{task_id}")
    builder.button(text="Нет", callback_data=f"{prefix}__Нет")
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


def delete_task_keyboard():
    builder = InlineKeyboardBuilder()
    reminders = get_reminders()
    for r in reminders:
        builder.button(text=str(r), callback_data=f"task__{r.task_id}")
    builder.button(text="Отменить", callback_data=f"task__")
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)

def memovoz_mng_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📝Статистика", callback_data="stat")],
            [InlineKeyboardButton(text="📝Статистика визитов", callback_data="visits")],
            [InlineKeyboardButton(text="📝Статистика по источникам", callback_data="sources")],
            [InlineKeyboardButton(text="Парсить", callback_data="parse")],
        ],
    )

def reminders_mng_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Добавить", callback_data="add_reminder")],
            [InlineKeyboardButton(text="Напоминания", callback_data="reminders")],
            [InlineKeyboardButton(text="Когда следующее?", callback_data="when_next")],
            [InlineKeyboardButton(text="Удалить напоминание", callback_data="delete")],
            [InlineKeyboardButton(text="Удалить все", callback_data="purge")],
        ],
    )
    
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
