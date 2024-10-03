import pytest
import os
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

from ..schemas.memes import MemeSchema
from .fake.fake_storage_repository import FakeStorageRepository
from ..config.app_config import MINIO_API_URL
from ..config.db_config import Base, get_db
from ..config.dependencies import get_storage_repo
from ..main import app

load_dotenv()

DB_USER: str = os.getenv("DB_USER")
DB_PASSWORD: str = os.getenv("DB_PASSWORD")
DB_HOST: str = os.getenv("DB_HOST", "localhost")
DB_PORT: str = os.getenv("DB_PORT", 5432)
# test db name
DB_NAME: str = os.getenv("TEST_DB_NAME")
DB_ENDPOINT: str = os.getenv("DB_ENDPOINT")

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)


engine = create_engine(SQLALCHEMY_DATABASE_URL)

if not database_exists(SQLALCHEMY_DATABASE_URL):
    create_database(SQLALCHEMY_DATABASE_URL)

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
    '''
    test FastApi client with overrided:
    - storage repository
    - database inside session

    '''
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    def override_get_storage_repo():
        return FakeStorageRepository(MINIO_API_URL)

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_storage_repo] = override_get_storage_repo
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="function")
def signup_user(test_client):
    '''
    signup user: dict
    and return JWT-token: str
    '''
    def _signup_user(test_user: dict) -> str:
        response = test_client.post("/auth/jwt/signup", data=test_user)
        print('response_signup', response.json())
        return response.json()['access_token']
    return _signup_user


@pytest.fixture(scope="function")
def login_user(test_client):
    '''
    login user: dict
    and return JWT-token: str
    '''
    def _login_user(test_user: dict) -> str:
        response = test_client.post("/auth/jwt/login", data=test_user)
        print('response_login', response.json())
        return response.json()['access_token']
    return _login_user


@pytest.fixture(scope="function")
def add_test_meme(test_client, login_user) -> list[MemeSchema]:
    '''
    - login user: dict
    - add file to storage: str
    - return list of memes: list[MemeSchema]
    '''
    def create_meme(file: dict, access_token: str):
        headers = {'Authorization': f'Bearer {access_token}'}
        with open("app/tests/fixtures/test_meme.jpg", "rb") as image_file:
            response = test_client.post(
                "/memes/",
                files={'file': ('init_filename', image_file)},
                data={'filename': file['name'], 'category': file['category']},
                headers=headers,
            )
            print('response.json()', response.json())
            return response.json()
    return create_meme
