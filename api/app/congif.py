import os

from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

MINIO_URL = os.getenv("MINIO_URL")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
MINIO_BUCKET = os.getenv("MINIO_BUCKET")

MINIO_API_URL = os.getenv("MINIO_API_URL")

TEST_DB_NAME = os.getenv("TEST_DB_NAME")
API_URL = os.getenv("API_URL")
TEST_ENV = os.getenv("TEST_ENV")

REACT_APP_API_URL = os.getenv("REACT_APP_API_URL")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_RESET_SECRET_KEY = os.getenv("JWT_RESET_SECRET_KEY")