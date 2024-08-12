from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .auth.auth import auth_backend
from .auth.manager import fastapi_users
from .auth.schemas import UserRead, UserCreate
from .routers.memes import router as router_memes

app = FastAPI()

origins = ['http://localhost:3000', ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router_memes)
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)