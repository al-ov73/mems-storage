from typing import Annotated

from fastapi import Depends, UploadFile, File, Form, APIRouter
from sqlalchemy.orm import Session

from ..config.db_config import get_db
from ..config.dependencies import get_storage_repo, get_memes_repository
from ..models.models import Meme
from ..repositories.memes_repository import MemesRepository
from ..repositories.storage_repository import BaseStorageRepo
from ..schemas.memes import MemeDbSchema, MemeSchema
from ..schemas.users import UserDbSchema
from ..utils.auth_utils import get_current_user

router = APIRouter()

@router.get(
    '/categories',
    # dependencies=[Depends(get_current_user)],
)
async def get_meme_category(
    db: Session = Depends(get_db),
    meme_repo: MemesRepository = Depends(get_memes_repository),
):
    """
    return list of memes categories
    """
    categories = db.execute("select enum_range(null::memes)")
    print('categories', categories)
    return 'categories'


@router.get(
    '',
    # dependencies=[Depends(get_current_user)],
)
async def get_memes(skip: int = 0,
                    limit: int = 100,
                    db: Session = Depends(get_db),
                    meme_repo: MemesRepository = Depends(get_memes_repository),
                    storage_repo: BaseStorageRepo = Depends(get_storage_repo),
                    ) -> list[MemeSchema]:
    """
    return list of memes with links to download
    """
    memes = await meme_repo.get_memes(skip, limit, db)
    for meme in memes:
        link = await storage_repo.get_link(meme.name)
        meme.link = link
    return memes




@router.get(
    '/{meme_id}',
    dependencies=[Depends(get_current_user)]
)
async def get_meme_link(meme_id: str,
                        db: Session = Depends(get_db),
                        meme_repo: MemesRepository = Depends(get_memes_repository),
                        storage_repo: BaseStorageRepo = Depends(get_storage_repo),
                        ) -> MemeSchema | str:
    """
    return meme with link to download
    """
    print('meme_id ->>', meme_id)
    meme = await meme_repo.get_meme(meme_id, db)
    if not meme:
        return 'meme not exist'
    meme.link = storage_repo.get_link(meme.name)
    return meme


@router.post('')
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
    try:
        current_user_id = user.id
        new_meme = Meme(
            name=filename,
            category=category,
            author_id=current_user_id
        )
        await storage_repo.add_image(filename, file.file)
        await meme_repo.add_meme(new_meme, db)
        return new_meme
    except Exception as e:
        return f'db error "{e}"'


@router.delete(
        '/{meme_id}',
        dependencies=[Depends(get_current_user)],
)
async def del_meme(
        meme_id: str,
        db: Session = Depends(get_db),
        meme_repo: MemesRepository = Depends(get_memes_repository),
        storage_repo: BaseStorageRepo = Depends(get_storage_repo),
) -> MemeSchema | MemeDbSchema | str:
    """
    delete meme from db and S3 storage
    """
    try:
        meme = await meme_repo.del_meme(meme_id, db)
        await storage_repo.delete_image(meme.name)
        return meme
    except Exception:
        return f'error "{Exception}"'


@router.put('/{meme_id}', dependencies=[Depends(get_current_user)],
)
async def update_meme(meme_id: str,
                      filename: Annotated[str, Form()],
                      file: UploadFile = File(...),
                      db: Session = Depends(get_db),
                      meme_repo: MemesRepository = Depends(get_memes_repository),
                      storage_repo: BaseStorageRepo = Depends(get_storage_repo),
                      ) -> MemeSchema | MemeDbSchema | str:
    """
    update meme in db and S3 storage
    """
    try:
        meme = await meme_repo.update_name(meme_id, filename, db)
        await storage_repo.update_image(old_name=meme.name, new_name=filename, new_file=file.file)
        return meme
    except Exception:
        return f'error "{Exception}"'
