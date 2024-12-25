import os

from dotenv import load_dotenv

load_dotenv()

ENV = os.getenv("ENV")
START_BOT = os.getenv("START_BOT")

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

# telegram bot config
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNELS = os.getenv("CHANNELS").split(" ")
CHAT_ID = os.getenv("CHAT_ID")
MY_API_ID = os.getenv("MY_API_ID")

# vk parser config
VK_TOKEN = os.getenv("VK_TOKEN")
VK_GROUPS = os.getenv("VK_GROUPS").split(" ")

PARSE_INTERVAL = os.getenv("PARSE_INTERVAL")
PARSE_LIMIT = os.getenv("PARSE_LIMIT")
SEND_PHOTO_INTERVAL = os.getenv("SEND_PHOTO_INTERVAL")
