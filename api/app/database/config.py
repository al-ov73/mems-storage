import os
from dotenv import load_dotenv

load_dotenv()

TEST_ENV = os.getenv("TEST_ENV")

if TEST_ENV == 'True':
    print('test db!!!!')
    class Settings:
        DB_USER: str = os.getenv("DB_USER")
        DB_PASSWORD = os.getenv("DB_PASSWORD")
        DB_HOST: str = os.getenv("DB_HOST", "localhost")
        DB_PORT: str = os.getenv("DB_PORT", 5432)
        DB_NAME: str = os.getenv("TEST_DB_NAME")
        DB_ENDPOINT: str = os.getenv("DB_ENDPOINT")
        DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?sslmode=require"

else:
    print('production DB!!!')
    class Settings:
        DB_USER : str = os.getenv("DB_USER")
        DB_PASSWORD = os.getenv("DB_PASSWORD")
        DB_HOST : str = os.getenv("DB_HOST", "localhost")
        DB_PORT : str = os.getenv("DB_PORT", 5432)
        DB_NAME : str = os.getenv("DB_NAME")
        DB_ENDPOINT : str = os.getenv("DB_ENDPOINT")
        DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?sslmode=require"

settings = Settings()
