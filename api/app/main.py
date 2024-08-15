from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel

from .auth.auth_handler import authenticate_user
from .models.schemas import Token
# from .auth.auth import auth_backend
# from .auth.manager import fastapi_users
# from .auth.schemas import UserRead, UserCreate, UserUpdate
from .routers.memes import router as router_memes
from .routers.auth import router as router_auth

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["*"],
)

app.include_router(
    router_auth,
    prefix="/auth/jwt",
    tags=["auth"],
)
app.include_router(
    router_memes,
    prefix="/memes",
    tags=["memes"],
)
