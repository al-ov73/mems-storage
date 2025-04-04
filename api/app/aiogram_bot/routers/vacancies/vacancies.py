import os

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import Message

from ...commands import TelegramCommands

from .keyboards import engineer_vacancies_keyboard, vacancies_mng_keyboard


vacancies_router = Router()


@vacancies_router.message(Command(commands=[TelegramCommands.VACANCIES.value.name]))
async def vacancies_handler(message: Message) -> None:
    await message.answer("Поиск вакансий:", reply_markup=vacancies_mng_keyboard())


@vacancies_router.callback_query(lambda c: c.data == "engineer")
async def parse_callback(callback_query: types.CallbackQuery):
    reply = await callback_query.message.answer("Последние вакансии", reply_markup=engineer_vacancies_keyboard())
