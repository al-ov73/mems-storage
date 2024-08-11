import os
from dotenv import load_dotenv

from ..congif import TEST_ENV, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, TEST_DB_NAME, DB_NAME

if TEST_ENV == 'True':
    print('test db!!!!')


    class Settings:
        DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{TEST_DB_NAME}"

else:
    print('production db!!!!')


    class Settings:
        DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

settings = Settings()
