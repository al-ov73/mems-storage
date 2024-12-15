from datetime import timedelta
from typing import Annotated, Optional

from fastapi import Depends, HTTPException, status, APIRouter, Form, UploadFile
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..utils.auth_utils import (
    authenticate_user,
    create_access_token,
    register_user
)
from ..config.db_config import get_db
from ..config.app_config import ACCESS_TOKEN_EXPIRE_MINUTES
from ..utils.auth_utils import get_current_user
from ..schemas.tokens import TokenSchema
from ..config.dependencies import get_storage_repo
from ..repositories.storage_repository import BaseStorageRepo


router = APIRouter()


@router.post("/login")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
) -> TokenSchema:
    '''
    check user in db, create and return JWT-token
    '''
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        user=user, expires_delta=access_token_expires
    )
    return TokenSchema(access_token=access_token, token_type="bearer")


@router.post("/signup")
async def signup_for_access_token(
    file: Optional[UploadFile] = None,
    username: str = Form(),
    password: str = Form(),
    first_name: str = Form(default=None),
    last_name: str = Form(default=None),
    db: Session = Depends(get_db),
    storage_repo: BaseStorageRepo = Depends(get_storage_repo),
) -> TokenSchema:
    '''
    add user in db, create and return JWT-token
    '''
    user_data = {
        'username': username,
        'password': password,
        'first_name': first_name,
        'last_name': last_name
    }
    user = await register_user(storage_repo, user_data, file, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        user=user, expires_delta=access_token_expires
    )
    return TokenSchema(access_token=access_token, token_type="bearer")


@router.get("/validate_token/{token}")
async def validate_token(
    token: str,
    db: Session = Depends(get_db),
) -> bool:
    '''
    validate token from frontend response
    '''
    user = await get_current_user(token, db)
    return True if user else False
