from enum import Enum

from aiogram.types import BotCommand
from dataclasses import dataclass


@dataclass
class TelegramCommand:
    name: str
    title: str

    @property
    def command(self) -> str:
        return f"/{self.name}"


class TelegramCommands(Enum):
    MEMOVOZ = TelegramCommand("memovoz", "Управление memovoz.ru")
    REMINDERS = TelegramCommand("reminders_mng", "Напоминания")
    VACANCIES = TelegramCommand("vacancies_mng", "Вакансии")


bot_commands = [BotCommand(command=c.value.command, description=c.value.title) for c in TelegramCommands]
