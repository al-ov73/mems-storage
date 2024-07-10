import os
from dotenv import load_dotenv

from pathlib import Path
# env_path = Path('.') / '.env'
# load_dotenv(dotenv_path=env_path)
load_dotenv()

class Settings:
    DB_USER : str = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST : str = os.getenv("DB_HOST", "localhost")
    DB_PORT : str = os.getenv("DB_PORT", 5432)
    DB_NAME : str = os.getenv("DB_NAME")
    DB_ENDPOINT : str = os.getenv("DB_ENDPOINT")
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?sslmode=require&options=endpoint={DB_ENDPOINT}"

settings = Settings()
