from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="📝Статистика", callback_data="stat"),
            InlineKeyboardButton(text="‼️Парсить‼️", callback_data="parse"),
            InlineKeyboardButton(text="👥Отпр. мем", callback_data="send"),
        ]
    ],
)
