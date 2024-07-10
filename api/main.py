from fastapi import Depends, HTTPException, status, APIRouter, Response, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from . import schemas, models
from typing import Optional, List


app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/', response_model=List[schemas.Meme])
def get_memes(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    memes = db.query(models.Meme).offset(skip).limit(limit).all()
    return memes


@app.post('/', response_model=schemas.Meme)
def create_meme(meme: schemas.CreateMeme, db: Session = Depends(get_db)):
    new_meme = models.Meme(**meme.dict())
    db.add(new_meme)
    db.commit()
    db.refresh(new_meme)
    return new_meme
