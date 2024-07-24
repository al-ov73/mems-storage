import os
from typing import Annotated

import requests
import sqlalchemy
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from api.app.database.database import SessionLocal
from api.app.models import models, schemas
from api.app.routers.memes import router as router_memes

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

app.include_router(router_memes)
#
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
#
# # @router.get('/', response_model=schemas.Meme)
# @app.get('/memes', response_model=list[schemas.Meme])
# async def get_memes(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
#     memes = db.query(models.Meme).offset(skip).limit(limit).all()
#     return memes
#
#
# @app.get('/memes/{meme_id}', response_model=schemas.MemeWithLink)
# async def get_meme_link(meme_id: str, db: Session = Depends(get_db)):
#     meme = db.get(models.Meme, meme_id)
#     if not meme:
#         return 'meme not exist'
#     response = requests.get(f'{storage_host}/link/{meme.name}')
#     link = response.text
#     return {
#         'meme': meme,
#         'link': link[1:-1],
#     }
#
#
# @app.post('/memes', response_model=schemas.Meme)
# async def upload_file(file: UploadFile, filename: str = Form(),
#                 db: Session = Depends(get_db)):
#     # add to db
#     try:
#         new_meme = models.Meme(name=filename)
#         new_meme.is_uploaded = False
#         if os.getenv("TEST_ENV") == 'False':
#             # add to s3
#             response = requests.post(f'{storage_host}/upload', files={
#                 'file': (filename, file.file, 'multipart/form-data')})
#             if response.status_code == 200:
#                 new_meme.is_uploaded = True
#         db.add(new_meme)
#         db.commit()
#         db.refresh(new_meme)
#         return new_meme
#     except sqlalchemy.exc.IntegrityError:
#         return f'file "{filename}" already exist in db'
#     except Exception as e:
#         return f'error "{e}"'
#
#
# @app.delete('/memes/{meme_id}', response_model=schemas.Meme)
# async def del_meme(meme_id: str, db: Session = Depends(get_db)):
#     # rm from db
#     try:
#         meme = db.get(models.Meme, meme_id)
#         db.delete(meme)
#         if os.getenv("TEST_ENV") == 'False':
#             requests.delete(f'{storage_host}/meme_delete/{meme.name}')
#         db.commit()
#         return meme.to_dict()
#     except Exception:
#         return f'error "{Exception}"'
#
#
# @app.put('/memes/{meme_id}', response_model=schemas.Meme)
# async def update_meme(meme_id: str, filename: Annotated[str, Form()],
#                 file: UploadFile = File(...), db: Session = Depends(get_db)):
#     # update in db
#     try:
#         meme = db.get(models.Meme, meme_id)
#         if os.getenv("TEST_ENV") == 'False':
#             # update in s3
#             delete_response = requests.delete(
#                 f'{storage_host}/meme_delete/{meme.name}')
#             upload_response = requests.post(f'{storage_host}/upload', files={
#                 'file': (filename, file.file, 'multipart/form-data')})
#         if meme.name != filename:
#             meme.name = filename
#         db.commit()
#         return meme.to_dict()
#     except Exception:
#         return f'error "{Exception}"'
