from typing import Annotated
from fastapi import Depends, Form, APIRouter, Request
from sqlalchemy.orm import Session
import httpx
from ..config import config

from ..config.logger_config import get_logger
from ..config.db_config import get_db
from ..config.dependencies import get_storage_repo, get_memes_repository
from ..models.meme import Meme
from ..parsers.telegram_parser import parse_telegram_channels
from ..repositories.memes_repository import MemesRepository
from ..repositories.storage_repository import BaseStorageRepo
from ..schemas.memes import MemeDbSchema
from ..schemas.stat import DayStatSchema, StatSchema

router = APIRouter()

logger = get_logger(__name__)


@router.get(
    "",
    # dependencies=[Depends(get_current_user)],
)
async def get_memes(
    skip: int = 0,
    limit: int = 2000,
    db: Session = Depends(get_db),
    meme_repo: MemesRepository = Depends(get_memes_repository),
    storage_repo: BaseStorageRepo = Depends(get_storage_repo),
):
    """
    return list of memes with links to download
    """
    logger.info("Got request for all memes")
    memes = await meme_repo.get_memes(skip, limit, db)
    return memes


@router.get(
    "/checked",
)
async def get_checked_memes(
    request: Request,
    skip: int = 0,
    limit: int = 2000,
    db: Session = Depends(get_db),
    meme_repo: MemesRepository = Depends(get_memes_repository),
    storage_repo: BaseStorageRepo = Depends(get_storage_repo),
):
    """
    return list of memes with links to download
    """
    memes = await meme_repo.get_checked_memes(skip, limit, db)
    headers = request.headers
    message = (f"{request.client.host}: {request.client.port} зашел на сайт\n\n"
                f"host: {headers.get("host")}\n"
                f"browser: {headers.get("sec-ch-ua")}\n"
                f"platform: {headers.get("sec-ch-ua-platform")}\n"
                f"mobile: {headers.get("sec-ch-ua-mobile")}\n"
               )
    telegram_api_url = f"https://api.telegram.org/bot{config.BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": config.MY_API_ID,
        "text": message,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(telegram_api_url, json=payload)
        
    return memes


@router.get(
    "/notchecked",
)
async def get_not_checked_memes(
    skip: int = 0,
    limit: int = 2000,
    db: Session = Depends(get_db),
    meme_repo: MemesRepository = Depends(get_memes_repository),
    storage_repo: BaseStorageRepo = Depends(get_storage_repo),
):
    """
    return list of memes with links to download
    """
    memes = await meme_repo.get_not_checked_memes(skip, limit, db)
    return memes


@router.post(
    "/check",
)
async def check_memes(
    ids: Annotated[str, Form()],
    db: Session = Depends(get_db),
    meme_repo: MemesRepository = Depends(get_memes_repository),
):
    """
    return list of memes with links to download
    """
    logger.info(f"Checked ids: {ids}")
    ids = list(map(lambda id: int(id), ids.split(" ")))
    checked_ids = await meme_repo.check_memes(ids, db)
    return checked_ids


@router.get("/parse")
async def parse_memes():
    await parse_telegram_channels()
    return {"result": "ok"}


# @router.get("/{meme_id}", dependencies=[Depends(get_current_user)])
# async def get_meme(
#     meme_id: str,
#     db: Session = Depends(get_db),
#     meme_repo: MemesRepository = Depends(get_memes_repository),
#     storage_repo: BaseStorageRepo = Depends(get_storage_repo),
# ) -> MemeSchema | str:
#     """
#     return meme with link to download
#     """
#     logger.info(f"Got request for meme {meme_id}")
#     meme = await meme_repo.get_meme(meme_id, db)
#     if not meme:
#         return "meme not exist"
#     meme.link = await storage_repo.get_link(meme.name)
#     return meme


@router.delete("/{meme_id}")
async def del_meme(
    meme_id: str,
    db: Session = Depends(get_db),
    meme_repo: MemesRepository = Depends(get_memes_repository),
    storage_repo: BaseStorageRepo = Depends(get_storage_repo),
) -> MemeDbSchema | str:
    """
    delete meme from db and S3 storage
    """
    meme = await meme_repo.del_meme(meme_id, db)
    await storage_repo.delete_image(meme.name)
    return meme


# @router.put("/{meme_id}", dependencies=[Depends(get_current_user)])
# async def update_meme(
#     meme_id: str,
#     filename: Annotated[str, Form()],
#     file: UploadFile = File(...),
#     db: Session = Depends(get_db),
#     meme_repo: MemesRepository = Depends(get_memes_repository),
#     storage_repo: BaseStorageRepo = Depends(get_storage_repo),
# ) -> MemeSchema | MemeDbSchema | str:
#     """
#     update meme in db and S3 storage
#     """
#     meme = await meme_repo.update_name(meme_id, filename, db)
#     await storage_repo.update_image(
#         old_name=meme.name, new_name=filename, new_file=file.file
#     )
#     return meme


@router.get(
    "/stat",
)
async def get_checked_memes(
    db: Session = Depends(get_db),
    meme_repo: MemesRepository = Depends(get_memes_repository),
) -> list[DayStatSchema]:
    """
    return day stat
    """
    memes = await meme_repo.get_memes_count_by_day(db)
    return memes

@router.get(
    "/count",
)
async def get_memes_count(
    db: Session = Depends(get_db),
    meme_repo: MemesRepository = Depends(get_memes_repository),
) -> StatSchema:
    """
    return day stat
    """
    stat = await meme_repo.get_published_stat(db)
    return stat
