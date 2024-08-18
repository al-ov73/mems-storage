from fastapi import APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import desc

from ..congif import MINIO_API_URL
from ..models.models import Meme

router = APIRouter(prefix='/memes')

storage_host = MINIO_API_URL


def get_memes(skip: int,
              limit: int,
              db: Session):
    memes = db.query(Meme).offset(skip).limit(limit).all()
    return memes


def get_meme(meme_id: str, db: Session):
    meme = db.get(Meme, meme_id)
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
        meme = db.get(Meme, meme_id)
        db.delete(meme)
        db.commit()
        return meme
    except Exception:
        return f'error "{Exception}"'


def update_name(meme_id: str,
                filename: str,
                db: Session):
    try:
        meme = db.get(Meme, meme_id)
        if meme.name != filename:
            meme.name = filename
        db.commit()
        return meme
    except Exception:
        return f'error "{Exception}"'
