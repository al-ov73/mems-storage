from datetime import datetime, timedelta, timezone
from typing import Annotated
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from ..config.app_congif import ALGORITHM, JWT_TOKEN_SECRET_KEY
from ..config.db_config import get_db
from ..models.models import User
from ..schemas.users import UserDbSchema
from ..schemas.tokens import TokenDataSchema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(
        plain_password: str,
        hashed_password: str
    ) -> bool:
    '''
    Check if user's password match saved password in db
    '''
    try:
        result = pwd_context.verify(plain_password, hashed_password)
    except Exception as ex:
        return False
    return result


def get_password_hash(password: str) -> str:
    '''
    hash password to save in db
    '''
    return pwd_context.hash(password)


def get_user(
        username: str,
        db: Session = Depends(get_db),
    ) -> UserDbSchema:
    '''
    return user from db
    '''
    user = db.query(User).filter(User.username == username).first()
    if user:
        return user


def authenticate_user(
        username: str,
        password: str,
        db: Session = Depends(get_db)
    ) -> UserDbSchema | None:
    '''
    return user if login and password match data in db
    '''
    user = get_user(username, db)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def register_user(
        username: str,
        password: str,
        db: Session = Depends(get_db)
    ) -> UserDbSchema | None:
    '''
    add user to db
    '''
    hashed_password = get_password_hash(password)
    new_user_dict = {
        'username': username,
        'hashed_password': hashed_password
    }
    new_user = User(**new_user_dict)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    if not new_user:
        return None
    return new_user


def create_access_token(
        data: dict,
        expires_delta: timedelta | None = None
    ) -> str:
    '''
    return JWT token with expires time
    '''
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_TOKEN_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        db: Session = Depends(get_db)
    ) -> UserDbSchema:
    '''
    return user from db according JWT-token data
    '''
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_TOKEN_SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenDataSchema(username=username)
    except InvalidTokenError:
        print('InvalidTokenError!!!')
        raise credentials_exception
    user = get_user(token_data.username, db)
    if user is None:
        raise credentials_exception
    return user