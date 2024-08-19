from datetime import timedelta
from typing import Annotated
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..utils.auth_utils import authenticate_user, create_access_token, register_user
from ..config.db_config import get_db
from ..config.app_congif import ACCESS_TOKEN_EXPIRE_MINUTES
from ..utils.auth_utils import get_current_user
from ..schemas.tokens import TokenSchema

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
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return TokenSchema(access_token=access_token, token_type="bearer")

@router.post("/signup")
async def signup_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: Session = Depends(get_db),
    ) -> TokenSchema:
    '''
    add user in db, create and return JWT-token
    '''
    user = register_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
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
