from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from redis import asyncio as aioredis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

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

# @app.on_event("startup")
# async def startup_event():
#     redis = aioredis.from_url("redis://localhost:5557", encoding="utf8", decode_responses=True)
#     FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
