from .. import schemas, models
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter, Response
from ..database import get_db

router = APIRouter()

@router.get('/', response_model=schemas.MemeResponse)
def get_memes(db: Session = Depends(get_db)):
    memes = db.query(models.Meme).all()
    return {'status': 'success', 'results': len(memes), 'memes': memes}


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.MemeResponse)
def create_meme(meme: schemas.CreateMemeSchema, db: Session = Depends(get_db)):
    new_meme = models.Meme(**meme.dict())
    db.add(new_meme)
    db.commit()
    db.refresh(new_meme)
    return new_meme