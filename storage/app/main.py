import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from .handlers.minio_handler import MinioHandler

load_dotenv()

app = FastAPI()

origins = [
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    'http://localhost',
    'http://127.0.0.1',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

storage_handler = MinioHandler(
    os.getenv('MINIO_URL'),
    os.getenv('MINIO_ACCESS_KEY'),
    os.getenv('MINIO_SECRET_KEY'),
    os.getenv('MINIO_BUCKET'),
    False
)


@app.post('/upload')
async def upload(request: Request):
    async with request.form() as form:
        filename = form['file'].filename
        size = form['file'].size
        contents = form['file'].file
        result = storage_handler.upload_file(filename, contents, size)
        return result


@app.get('/list')
async def list_files():
    return storage_handler.list()


@app.get('/link/{filename}')
async def get_link(filename: str):
    link = storage_handler.get_link(filename)
    return link


@app.delete('/meme_delete/{filename}')
async def delete_meme(filename: str):
    response = storage_handler.remove_object(filename)
    return response
