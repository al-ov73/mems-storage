# TODO
# docker compose
# запросы в бд в отдельный слой
# оформить readme
# фронт с карточками

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers.memes import router as router_memes

load_dotenv()

app = FastAPI()

origins = ['http://localhost:3000', ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router_memes)
