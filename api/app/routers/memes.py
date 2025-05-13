from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, Form, Request
from sqlalchemy.orm import Session

from ..config.db_config import get_db
from ..config.dependencies import get_memes_repository, get_storage_repo
from ..config.logger_config import get_logger
from ..parsers.telegram_parser import parse_telegram_channels
from ..repositories.memes_repository import MemesRepository
from ..repositories.storage_repository import BaseStorageRepo
from ..schemas.memes import MemeDbSchema
from ..schemas.stat import MemesDayStatSchema, StatSchema
from ..utils.tasks import send_visit_info_to_db

router = APIRouter()

logger = get_logger(__name__)


@router.get(
    "",
)
async def get_memes(
    skip: int = 0,
    limit: int = 2000,
    db: Session = Depends(get_db),
    meme_repo: MemesRepository = Depends(get_memes_repository),
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
    background_tasks: BackgroundTasks,
    skip: int = 0,
    limit: int = 2000,
    db: Session = Depends(get_db),
    meme_repo: MemesRepository = Depends(get_memes_repository),
):
    """
    return list of memes with links to download
    """
    logger.info("api request '/checked'")
    memes = await meme_repo.get_checked_memes(skip, limit, db)
    background_tasks.add_task(send_visit_info_to_db, request)
    return memes


@router.get(
    "/notchecked",
)
async def get_not_checked_memes(
    skip: int = 0,
    limit: int = 2000,
    db: Session = Depends(get_db),
    meme_repo: MemesRepository = Depends(get_memes_repository),
):
    """
    return list of memes with links to download
    """
    logger.info("api request '/notchecked'")
    memes = await meme_repo.get_not_checked_memes(skip, limit, db)
    return memes


@router.post(
    "/check",
)
async def check_memes(
    ids: Annotated[str, Form()],
    db: Session = Depends(get_db),
    meme_repo: MemesRepository = Depends(get_memes_repository),
) -> list[int]:
    """
    return list of memes with links to download
    """
    logger.info("api request '/check'")
    logger.info(f"Checked ids from client: {ids}")
    ids = list(map(lambda id: int(id), ids.split(" ")))
    checked_ids = await meme_repo.check_memes(ids, db)
    logger.info(f"Response from db: Checked ids {' '.join(map(str, checked_ids))}")
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
) -> list[MemesDayStatSchema]:
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


@router.get(
    "/day_count",
)
async def get_memes_count_by_day(
    db: Session = Depends(get_db),
    meme_repo: MemesRepository = Depends(get_memes_repository),
) -> list[MemesDayStatSchema]:
    """
    return day stat
    """
    days_stat = await meme_repo.get_memes_count_by_day(db)
    return days_stat


@router.get(
    "/add_preview",
)
async def add_preview(
    db: Session = Depends(get_db),
    meme_repo: MemesRepository = Depends(get_memes_repository),
):
    """
    return list of memes with links to download
    """
    logger.info("api request '/add_preview'")
    memes = await meme_repo.add_preview_if_not_exist(db)
    return memes
