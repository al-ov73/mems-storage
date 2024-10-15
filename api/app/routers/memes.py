from typing import Annotated
from fastapi import Depends, UploadFile, File, Form, APIRouter, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from ..config.logger_config import get_logger
from ..config.db_config import get_db
from ..config.dependencies import get_storage_repo, get_memes_repository
from ..models.meme import Meme
from ..repositories.memes_repository import MemesRepository
from ..repositories.storage_repository import BaseStorageRepo
from ..schemas.memes import MemeDbSchema, MemeSchema
from ..schemas.users import UserDbSchema
from ..utils.auth_utils import get_current_user

router = APIRouter()

logger = get_logger(__name__)


@router.get(
    "/categories",
    dependencies=[Depends(get_current_user)],
)
async def get_meme_category(
    db: Session = Depends(get_db),
):
    """
    return list of memes categories
    """
    categories = []
    query = db.execute(text("select unnest(enum_range(null::categoryenum))"))
    result = query.fetchall()
    for category in result:
        categories.append(category[0])
    return categories

@router.get(
    "/top_liked_memes",
    # dependencies=[Depends(get_current_user)],
)
async def get_top_liked_memes(
    limit: int = 100,
    db: Session = Depends(get_db),
    meme_repo: MemesRepository = Depends(get_memes_repository),
    storage_repo: BaseStorageRepo = Depends(get_storage_repo),
):
    """
    return list of memes with links to download
    """
    logger.info("Got request for top liked memes")
    memes = await meme_repo.get_top_liked_memes(limit, db)
    print('type memes', type(memes))
    print('type 1 meme', type(memes[0]))
    # print('memes', memes)
    for meme in memes:
        print(meme)
        # row = meme.fetchone()
        dict_row = dict(meme)
        print(dict_row)
    #     link = await storage_repo.get_link(meme.id)
    #     meme.link = link
    return memes


@router.get(
    "",
    dependencies=[Depends(get_current_user)],
)
async def get_memes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    meme_repo: MemesRepository = Depends(get_memes_repository),
    storage_repo: BaseStorageRepo = Depends(get_storage_repo),
):
    """
    return list of memes with links to download
    """
    logger.info("Got request for all memes")
    memes = await meme_repo.get_memes(skip, limit, db)
    logger.debug(f"Got {len(memes)} memes from db")
    for meme in memes:
        link = await storage_repo.get_link(meme.id)
        meme.link = link
    return memes


@router.get("/{meme_id}", dependencies=[Depends(get_current_user)])
async def get_meme(
    meme_id: str,
    db: Session = Depends(get_db),
    meme_repo: MemesRepository = Depends(get_memes_repository),
    storage_repo: BaseStorageRepo = Depends(get_storage_repo),
) -> MemeSchema | str:
    """
    return meme with link to download
    """
    logger.info(f"Got request for meme {meme_id}")
    meme = await meme_repo.get_meme(meme_id, db)
    if not meme:
        return "meme not exist"
    meme.link = await storage_repo.get_link(meme.name)
    return meme


@router.post("")
async def upload_file(
    file: UploadFile,
    filename: str = Form(),
    category: str = Form(),
    db: Session = Depends(get_db),
    meme_repo: MemesRepository = Depends(get_memes_repository),
    storage_repo: BaseStorageRepo = Depends(get_storage_repo),
    user: UserDbSchema = Depends(get_current_user),
) -> MemeDbSchema | str:
    """
    add meme to db and to S3 storage
    """
    logger.info(f"Got request for from user {user.id}:{user.username}")
    logger.info(f"File: {type(file)}, category: {category}")
    current_user_id = user.id
    new_meme = Meme(
        name=filename,
        category=category,
        author_id=current_user_id
    )
    meme_in_db = await meme_repo.add_meme(new_meme, db)
    logger.info(f"loaded meme to db {meme_in_db.id}")
    meme_name_in_storage = str(meme_in_db.id)
    await storage_repo.add_image(meme_name_in_storage, file.file)
    return meme_in_db


@router.delete(
    "/{meme_id}",
)
async def del_meme(
    meme_id: str,
    db: Session = Depends(get_db),
    meme_repo: MemesRepository = Depends(get_memes_repository),
    storage_repo: BaseStorageRepo = Depends(get_storage_repo),
    user: UserDbSchema = Depends(get_current_user),
) -> MemeDbSchema | str:
    """
    delete meme from db and S3 storage
    """
    meme = await meme_repo.get_meme(meme_id, db)
    print("meme to delete", meme)
    print("meme.author id", meme.author_id)
    print('request user', user.id)
    author_id = meme.author_id
    if user.id != author_id:
        raise HTTPException(
            status_code=403,
            detail="You don't have permissions to delete this meme"
        )
    meme = await meme_repo.del_meme(meme_id, db)
    await storage_repo.delete_image(meme.name)
    return meme


@router.put("/{meme_id}", dependencies=[Depends(get_current_user)])
async def update_meme(
    meme_id: str,
    filename: Annotated[str, Form()],
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    meme_repo: MemesRepository = Depends(get_memes_repository),
    storage_repo: BaseStorageRepo = Depends(get_storage_repo),
) -> MemeSchema | MemeDbSchema | str:
    """
    update meme in db and S3 storage
    """
    meme = await meme_repo.update_name(meme_id, filename, db)
    await storage_repo.update_image(
        old_name=meme.name, new_name=filename, new_file=file.file
    )
    return meme
