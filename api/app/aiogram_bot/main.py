from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.filters.command import Command
from aiogram.types import Message, ReplyKeyboardMarkup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import CallbackQuery
import asyncio
from ..config import app_config as config
from ...parse import parse


bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")
    test_kb = InlineKeyboardMarkup()
    test_kb_1 = InlineKeyboardButton(text="Первая кнопка", callback_data="first_one")
    test_kb.add(test_kb_1)
    await message.answer("Кнопки:", reply_markup=test_kb)


@dp.message(Command('parse'))
async def parse_command(message: Message):
    await message.answer("Вы вызвали команду parse")
    count = await parse()
    await message.answer(f"count: {count}")

async def start_bot():
    loop = asyncio.get_event_loop()
    loop.create_task(dp.start_polling(bot))