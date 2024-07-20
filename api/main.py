import sqlalchemy
from fastapi import Depends, FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
from sqlalchemy.orm import Session

from . import models
from .database import SessionLocal

import requests
import os
from dotenv import load_dotenv

load_dotenv()

storage_host = os.getenv('MINIO_API_URL')

app = FastAPI()

origins = ['http://localhost:3000', ]

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


@app.get('/memes')
def get_memes(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    memes = db.query(models.Meme).offset(skip).limit(limit).all()
    return memes


@app.get('/memes/{meme_id}')
def get_meme_link(meme_id: str, db: Session = Depends(get_db)):
    meme = db.get(models.Meme, meme_id)
    response = requests.get(f'{storage_host}/link/{meme.name}')
    link = response.text
    return link[1:-1]


@app.post('/memes')
def upload_file(file: UploadFile, filename: str = Form(),
                db: Session = Depends(get_db)):
    # add to db
    try:
        new_meme = models.Meme(name=filename)
        db.add(new_meme)
        # add to s3
        response = requests.post(f'{storage_host}/upload', files={
            'file': (filename, file.file, 'multipart/form-data')})
        db.commit()
        db.refresh(new_meme)
        if response.status_code == 200:
            return f'file {filename} uploaded'
    except sqlalchemy.exc.IntegrityError:
        return f'file "{filename}" already exist in db'
    except Exception:
        return f'error "{Exception}"'


@app.delete('/memes/{meme_id}')
def del_meme(meme_id: str, db: Session = Depends(get_db)):
    # rm from db
    try:
        meme = db.get(models.Meme, meme_id)
        db.delete(meme)
        response = requests.delete(f'{storage_host}/meme_delete/{meme.name}')
        if response.status_code == 200:
            db.commit()
            return f'file {meme.name} removed'
    except Exception:
        return f'error "{Exception}"'


@app.put('/memes/{meme_id}')
def update_meme(meme_id: str, filename: Annotated[str, Form()],
                file: UploadFile = File(...), db: Session = Depends(get_db)):
    # update in db
    try:
        meme = db.get(models.Meme, meme_id)
        # update in s3
        delete_response = requests.delete(
            f'{storage_host}/meme_delete/{meme.name}')
        upload_response = requests.post(f'{storage_host}/upload', files={
            'file': (filename, file.file, 'multipart/form-data')})
        if meme.name != filename:
            meme.name = filename
        db.commit()
        if delete_response.status_code == upload_response.status_code == 200:
            return f'file {file.filename} updated'
    except Exception:
        return f'error "{Exception}"'
