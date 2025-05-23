import asyncio
import logging
import os
import uuid

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqladmin import Admin
from starlette.middleware.base import BaseHTTPMiddleware

from .admin import AdminAuth, admin_views
from .aiogram_bot.main import start_bot
from .config import config
from .config.config import ORIGINS
from .config.db_config import engine
from .routers.aichat import router as router_aichat
from .routers.auth import router as router_auth
from .routers.chat import router as router_chat
from .routers.comments import router as router_comments
from .routers.labels import router as router_labels
from .routers.likes import router as router_likes
from .routers.memes import router as router_memes
from .routers.pdf import router as router_pdf
from .routers.support import router as router_support
from .routers.users import router as router_users

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

if config.ENV == "prod":
    file_handler = logging.FileHandler("logfile.txt")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
    logger.addHandler(file_handler)


app = FastAPI()

os.makedirs("uploads", exist_ok=True)
os.makedirs("static", exist_ok=True)

user_sessions = {}


class SessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        session_id = request.cookies.get("session_id")
        if session_id in user_sessions:
            request.state.session = user_sessions[session_id]
        elif session_id is None:
            new_session_id = str(uuid.uuid4())
            request.state.session = {}
            user_sessions[new_session_id] = request.state.session
            session_id = new_session_id
        else:
            request.state.session = {}
            user_sessions[session_id] = request.state.session

        response = await call_next(request)

        if request.cookies.get("session_id") is None:
            cookie_life = 15 * 60
            response.set_cookie(
                key="session_id",
                value=session_id,
                httponly=True,
                max_age=cookie_life,
            )

        return response


app.add_middleware(SessionMiddleware)

authentication_backend = AdminAuth(secret_key="secret")

admin = Admin(app, engine, authentication_backend=authentication_backend)

for admin_view in admin_views:
    admin.add_view(admin_view)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=config.STATIC_DIR), config.STATIC_URL)

if bool(config.START_BOT):

    @app.on_event("startup")
    async def on_startup():
        asyncio.create_task(start_bot())


app.include_router(router_auth, prefix="/auth/jwt", tags=["auth"])
app.include_router(router_memes, prefix="/memes", tags=["memes"])
app.include_router(router_labels, prefix="/labels", tags=["labels"])
app.include_router(router_comments, prefix="/comments", tags=["comments"])
app.include_router(router_likes, prefix="/likes", tags=["likes"])
app.include_router(router_chat, prefix="/chat", tags=["chat"])
app.include_router(router_users, prefix="/users", tags=["users"])
app.include_router(router_aichat, prefix="/question", tags=["aichat"])
app.include_router(router_support, prefix="/support", tags=["support"])
app.include_router(router_pdf, prefix="/pdf", tags=["pdf"])
