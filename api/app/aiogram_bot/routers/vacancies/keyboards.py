from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

from ....parsers.hh_parser import Vacancy, search_vacancies


def vacancies_mng_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Инженер", callback_data="engineer")],
        ],
    )


def engineer_vacancies_keyboard() -> InlineKeyboardButton:
    vacancies: list[Vacancy] = search_vacancies()
    builder = InlineKeyboardBuilder()
    for v in vacancies:
        builder.button(text=f"{v.name} - {v.employer['name']}", web_app=WebAppInfo(url=v.url))
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)
