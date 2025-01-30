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
    PARSE = TelegramCommand("parse", "Парсить")
    STAT = TelegramCommand("stat", "Статистика")
    SOURCES = TelegramCommand("sources", "Статистика по источникам")
    SEND = TelegramCommand("send", "Отправить мем")
    VISITS = TelegramCommand("visits", "Статистика визитов")


bot_commands = [BotCommand(command=c.value.command, description=c.value.title) for c in TelegramCommands]
