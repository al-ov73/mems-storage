import os
from base64 import b64encode
from pathlib import Path

import pytz
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv
from fastapi.templating import Jinja2Templates
from tinydb import TinyDB

load_dotenv()

ENV = os.getenv("ENV")
START_BOT = os.getenv("START_BOT")  # 1 - start bot, '' - bot no need

ORIGINS = os.getenv("ORIGINS", "").split(",")

# Postgress config
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Minio config
MINIO_URL = os.getenv("MINIO_URL")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
MINIO_BUCKET = os.getenv("MINIO_BUCKET")

# Url config
REACT_APP_API_URL = os.getenv("REACT_APP_API_URL")
MINIO_API_URL = os.getenv("MINIO_API_URL")
API_URL = os.getenv("API_URL")
REDIS_URL = os.getenv("REDIS_URL")

# JWT Token config
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_RESET_SECRET_KEY = os.getenv("JWT_RESET_SECRET_KEY")
JWT_TOKEN_SECRET_KEY = os.getenv("JWT_TOKEN_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120

# Static files directory
STATIC_DIR = "app/static"
PHOTOS_DIR = (f"{STATIC_DIR}/photos",)
STATIC_URL = "static"
PHOTOS_URL = f"{STATIC_URL}/photos"

# parser config
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
CHANNEL = os.getenv("CHANNEL")
YA_TOKEN = os.getenv("YA_TOKEN")

# parser intervals
PARSE_INTERVAL = int(os.getenv("PARSE_INTERVAL"))
PARSE_LIMIT = int(os.getenv("PARSE_LIMIT"))
SEND_PHOTO_INTERVAL = int(os.getenv("SEND_PHOTO_INTERVAL"))

# telegram bot config
NOT_CHECKED_URL = "https://memovoz.ru/temp"
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNELS = os.getenv("CHANNELS").split(" ")
CHAT_ID = os.getenv("CHAT_ID")
MY_API_ID = os.getenv("MY_API_ID")
SEND_BOT_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
LOCAL_IPS = os.getenv("LOCAL_IPS").split(" ")
tiny_db = TinyDB("db.json")
API_TOKEN = os.getenv("BOT_TOKEN")
timezone = pytz.timezone("Etc/GMT-4")

scheduler = AsyncIOScheduler()
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

remainder_types = {
    "Один раз": "one_time",
    "Ежедневно": "daily",
    "Еженедельно": "weekly",
    "Каждые 2 недели": "two_weeks",
    "Ежемесячно": "monthly",
}

months = {
    "ЯНВ": 1,
    "ФЕВ": 2,
    "МАР": 3,
    "АПР": 4,
    "МАЙ": 5,
    "ИЮН": 6,
    "ИЮЛ": 7,
    "АВГ": 8,
    "СЕН": 9,
    "ОКТ": 10,
    "НОЯ": 11,
    "ДЕК": 12,
}

# vk parser config
VK_TOKEN = os.getenv("VK_TOKEN")
VK_GROUPS = os.getenv("VK_GROUPS").split(" ")

# gigachat config
GIGACHAT_KEY = os.getenv("GIGACHAT_KEY")
JOKE_INTERVAL = os.getenv("JOKE_INTERVAL")

LEFT_TOP_COORDS = (54.377198, 48.616981)
RIGHT_BOTTOM_COORDS = (54.356967, 48.712990)
VACANCY_TEXT = "инженер"

templates = Jinja2Templates(directory=str(Path(__file__).parent.parent / "templates"))
templates.env.filters["b64encode"] = lambda x: b64encode(x).decode("utf-8")
