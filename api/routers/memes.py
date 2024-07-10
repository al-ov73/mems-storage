from .. import schemas, models
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter, Response
from ..database import get_db
from sqlalchemy.orm import Session

@router.get('/', response_model=schemas.Meme)
def get_memes(db: Session, skip: int = 0, limit: int = 100):
    memes = db.query(models.Meme).offset(skip).limit(limit).all()
    return {'status': 'success', 'results': len(memes), 'memes': memes}


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Meme)
def create_meme(db: Session, meme: schemas.CreateMeme):
    new_meme = models.Meme(**meme.dict())
    db.add(new_meme)
    db.commit()
    db.refresh(new_meme)
    return new_meme
