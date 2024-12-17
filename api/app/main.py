import asyncio
from fastapi import FastAPI
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from .aiogram_bot.main import start_bot


from .parsers.telegram_parser import parse_telegram_channels

from .config.app_config import STATIC_DIR, STATIC_URL

from .routers.auth import router as router_auth
from .routers.memes import router as router_memes
from .routers.labels import router as router_labels
from .routers.comments import router as router_comments
from .routers.likes import router as router_likes
from .routers.users import router as router_users
from .routers.aichat import router as router_aichat


app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://45.80.71.178:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=STATIC_DIR), STATIC_URL)


@app.on_event("startup")
async def on_startup():
    asyncio.create_task(start_bot())


app.include_router(router_auth, prefix="/auth/jwt", tags=["auth"])
app.include_router(router_memes, prefix="/memes", tags=["memes"])
app.include_router(router_labels, prefix="/labels", tags=["labels"])
app.include_router(router_comments, prefix="/comments", tags=["comments"])
app.include_router(router_likes, prefix="/likes", tags=["likes"])
app.include_router(router_users, prefix="/users", tags=["users"])
app.include_router(router_aichat, prefix="/question", tags=["aichat"])
