import os

import httpx
import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..config.db_config import Base, engine, get_db
from ..main import app

load_dotenv()

DB_USER: str = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST: str = os.getenv("DB_HOST", "localhost")
DB_PORT: str = os.getenv("DB_PORT", 5432)
DB_NAME: str = os.getenv("TEST_DB_NAME")
DB_ENDPOINT: str = os.getenv("DB_ENDPOINT")
SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?sslmode=require"


engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False,
                                   bind=engine)

Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """
    Create a new database session with a rollback at the end of the test.
    """
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def test_client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="function")
def login_user(test_client):
    def _login_user(test_user: dict):
        test_client.post("/auth/jwt/signup", data=test_user)
        response = test_client.post("/auth/jwt/login", data=test_user)
        return response.json()['access_token']
    return _login_user

@pytest.fixture(scope="function")
def add_test_meme(test_client, login_user):
    def create_meme(filename: str):
        with open("api/app/tests/fixtures/test_meme.jpg", "rb") as image_file:
            response = test_client.post(
                "/memes/",
                files={'file': ('init_filename', image_file)},
                data={'filename': filename},
            )
            return response.json()
    return create_meme
