from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from ..congif import TEST_ENV, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, TEST_DB_NAME, DB_NAME

if TEST_ENV == 'True':
    class Settings:
        DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{TEST_DB_NAME}"

else:
    class Settings:
        DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

settings = Settings()

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
