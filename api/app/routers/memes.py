import os
from typing import Annotated

import requests
from fastapi import Depends, UploadFile, File, Form, APIRouter
from sqlalchemy.orm import Session

from ..congif import MINIO_API_URL
from ..database import crud

from ..models import models, schemas
from ..models.models import User
from ..auth.auth_handler import get_current_user
from ..database.database import get_db

router = APIRouter()

@router.get('', response_model=list[schemas.Meme])
async def get_memes(current_user: Annotated[User, Depends(get_current_user)],
                    skip: int = 0,
                    limit: int = 100,
                    db: Session = Depends(get_db)):
    memes = crud.get_memes(skip, limit, db)
    for meme in memes:
        response = requests.get(f'{MINIO_API_URL}/link/{meme.name}')
        link = response.text
        meme.link = link[1:-1]
    return memes


@router.get('/{meme_id}')
async def get_meme_link(meme_id: str,
                        db: Session = Depends(get_db)):
    meme = crud.get_meme(meme_id, db)
    if not meme:
        return 'meme not exist'
    response = requests.get(f'{MINIO_API_URL}/link/{meme.name}')
    link = response.text
    return {
        'meme': meme,
        'link': link[1:-1],
    }


@router.post('')
async def upload_file(file: UploadFile, filename: str = Form(),
                      db: Session = Depends(get_db)):
    try:
        new_meme = models.Meme(name=filename)
        new_meme.is_uploaded = False
        if os.getenv("TEST_ENV") == 'False':
            response = requests.post(f'{MINIO_API_URL}/upload', files={
                'file': (filename, file.file, 'multipart/form-data')})
            if response.status_code == 200:
                new_meme.is_uploaded = True
            crud.add_meme(new_meme, db)
            return new_meme
        else:
            crud.add_meme(new_meme, db)
            return new_meme
    except Exception as e:
        return f'db error "{e}"'


@router.delete('/{meme_id}', response_model=schemas.DeleteMeme)
async def del_meme(meme_id: str, db: Session = Depends(get_db)):
    try:
        meme = crud.del_meme(meme_id, db)
        if os.getenv("TEST_ENV") == 'False':
            # del from s3
            requests.delete(f'{MINIO_API_URL}/meme_delete/{meme.name}')
        return meme.to_dict()
    except Exception:
        return f'error "{Exception}"'


@router.put('/{meme_id}', response_model=schemas.Meme)
async def update_meme(meme_id: str,
                      filename: Annotated[str, Form()],
                      file: UploadFile = File(...),
                      db: Session = Depends(get_db)):
    try:
        meme = crud.update_name(meme_id, filename, db)
        if os.getenv("TEST_ENV") == 'False':
            # update in s3
            delete_response = requests.delete(
                f'{MINIO_API_URL}/meme_delete/{meme.name}')
            upload_response = requests.post(f'{MINIO_API_URL}/upload', files={
                'file': (filename, file.file, 'multipart/form-data')})
        return meme.to_dict()
    except Exception:
        return f'error "{Exception}"'
