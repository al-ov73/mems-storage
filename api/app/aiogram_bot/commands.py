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
    STAT = TelegramCommand("stat", "Статистика")
    VISITS = TelegramCommand("visits", "Статистика визитов")
    SOURCES = TelegramCommand("sources", "Статистика по источникам")
    PARSE = TelegramCommand("parse", "Парсить")
    SEND = TelegramCommand("send", "Отправить мем")


bot_commands = [BotCommand(command=c.value.command, description=c.value.title) for c in TelegramCommands]
