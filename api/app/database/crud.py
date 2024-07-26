import os

from dotenv import load_dotenv
from fastapi import APIRouter
from sqlalchemy.orm import Session

from ..models import models

load_dotenv()

router = APIRouter(prefix='/memes')

storage_host = os.getenv('MINIO_API_URL')


def get_memes(skip: int,
              limit: int,
              db: Session):
    memes = db.query(models.Meme).offset(skip).limit(limit).all()
    return memes


def get_meme(meme_id: str, db: Session):
    meme = db.get(models.Meme, meme_id)
    if not meme:
        return 'meme not exist'
    return meme


def add_meme(new_meme, db: Session):
    db.add(new_meme)
    db.commit()
    db.refresh(new_meme)
    return new_meme


def del_meme(meme_id: str, db: Session):
    try:
        meme = db.get(models.Meme, meme_id)
        db.delete(meme)
        db.commit()
        return meme
    except Exception:
        return f'error "{Exception}"'


def update_name(meme_id: str,
                filename: str,
                db: Session):
    try:
        meme = db.get(models.Meme, meme_id)
        if meme.name != filename:
            meme.name = filename
        db.commit()
        return meme
    except Exception:
        return f'error "{Exception}"'
