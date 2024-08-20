import os

from typing import Annotated
from fastapi import Depends, UploadFile, File, Form, APIRouter
from sqlalchemy.orm import Session
import requests

from ..models.models import Meme
from ..schemas.memes import MemeDbSchema, MemeSchema
from ..repositories.memes_repository import MemesRepository
from ..config.app_congif import MINIO_API_URL
from ..config.db_config import get_db
from ..utils.auth_utils import get_current_user

router = APIRouter()

MEME_REPO = MemesRepository()


@router.get(
    '',
    response_model=list[MemeSchema],
    dependencies=[Depends(get_current_user)],
)
async def get_memes(skip: int = 0,
                    limit: int = 100,
                    db: Session = Depends(get_db)
                    ):
    """
    return list of memes with links to download
    """
    memes = await MEME_REPO.get_memes(skip, limit, db)
    for meme in memes:
        response = requests.get(f'{MINIO_API_URL}/images/{meme.name}')
        link = response.text
        meme.link = link[1:-1]
    return memes


@router.get('/{meme_id}', dependencies=[Depends(get_current_user)], )
async def get_meme_link(meme_id: str,
                        db: Session = Depends(get_db)
                        ) -> MemeSchema:
    """
    return meme with link to download
    """
    meme = await MEME_REPO.get_meme(meme_id, db)
    if not meme:
        return 'meme not exist'
    response = requests.get(f'{MINIO_API_URL}/images/{meme.name}')
    meme.link = response.text
    return meme


@router.post('', dependencies=[Depends(get_current_user)], )
async def upload_file(
        file: UploadFile,
        filename: str = Form(),
        db: Session = Depends(get_db)
) -> MemeSchema | MemeDbSchema| str:
    """
    add meme to db and to S3 storage
    """
    try:
        new_meme = Meme(name=filename)
        if os.getenv("TEST_ENV") == 'False':
            response = requests.post(f'{MINIO_API_URL}/images', files={
                'file': (filename, file.file, 'multipart/form-data')})
            if response.status_code != 200:
                return 'storage error'
            await MEME_REPO.add_meme(new_meme, db)
            return new_meme
        else:
            await MEME_REPO.add_meme(new_meme, db)
            return new_meme
    except Exception as e:
        return f'db error "{e}"'


@router.delete(
    '/{meme_id}',
    dependencies=[Depends(get_current_user)],
)
async def del_meme(
        meme_id: str,
        db: Session = Depends(get_db)
) -> MemeSchema | MemeDbSchema| str:
    """
    delete meme from db and S3 storage
    """
    try:
        meme = await MEME_REPO.del_meme(meme_id, db)
        if os.getenv("TEST_ENV") == 'False':
            # del from s3
            requests.delete(f'{MINIO_API_URL}/images/{meme.name}')
        return meme
    except Exception:
        return f'error "{Exception}"'


@router.put(
    '/{meme_id}',
    dependencies=[Depends(get_current_user)],
)
async def update_meme(meme_id: str,
        filename: Annotated[str, Form()],
        file: UploadFile = File(...),
        db: Session = Depends(get_db)
    ) -> MemeSchema | MemeDbSchema| str:
    """
    update meme in db and S3 storage
    """
    try:
        meme = await MEME_REPO.update_name(meme_id, filename, db)
        if os.getenv("TEST_ENV") == 'False':
            # update in s3
            requests.delete(f'{MINIO_API_URL}/images/{meme.name}')
            requests.post(f'{MINIO_API_URL}/images', files={
                'file': (filename, file.file, 'multipart/form-data')
            })
        return meme
    except Exception:
        return f'error "{Exception}"'
