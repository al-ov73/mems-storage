from httpx import request
from fastapi import Depends, FastAPI, UploadFile, File, FastAPI, File, Form, UploadFile
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware

from api import schemas, models
from .config import settings
from sqlalchemy.orm import Session
from .database import SessionLocal, engine

from typing import Optional, List
import requests
from minio import Minio
import os
import json
from dotenv import load_dotenv
import shutil


load_dotenv()

storage_host = os.getenv('MINIO_API_URL')


app = FastAPI()

origins = ['http://localhost:3000',]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/')
def get_memes(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    response = requests.get(f'{storage_host}/list')
    return { 'response from storage': json.loads(response.content) }


@app.post('/')
def upload_file_bytes(db: Session = Depends(get_db), file: UploadFile = File(...)):
    s = requests.Session()
    response = s.post(f'{storage_host}/upload', files={'file': (file.filename, file.file, 'multipart/form-data')})
    return {
        'url:': response,
    }

     
    
    # new_meme = models.Meme(**meme.dict())
    # db.add(new_meme)
    # db.commit()
    # db.refresh(new_meme)
    # return new_meme
