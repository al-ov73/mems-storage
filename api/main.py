from fastapi import Depends, FastAPI, UploadFile, File, FastAPI, File, Form, UploadFile
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from . import schemas, models
from typing import Optional, List
import requests

app = FastAPI()

origins = ['http://localhost:3001',
    'https://localhost:3001',
    'http://localhost:8000',
    'https://localhost:8000',
    'http://127.0.0.1:3001/',
    'http://127.0.0.1:3001',
    'http://127.0.0.1:8000/'
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

STORAGE_URL = 'http://127.0.0.1:9001'

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
    img_list = requests.get(f'{STORAGE_URL}/list')
    print('img_list', img_list)
    return memes


@app.post('/')
def upload_file_bytes(file: UploadFile = File(...)):
    return {"filename": file}
    
    # new_meme = models.Meme(**meme.dict())
    # db.add(new_meme)
    # db.commit()
    # db.refresh(new_meme)
    # return new_meme
