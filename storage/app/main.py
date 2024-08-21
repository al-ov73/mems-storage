import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request

from .handlers.minio_handler import MinioHandler

load_dotenv()

app = FastAPI()

MINIO_BUCKET = os.getenv('MINIO_BUCKET') if os.getenv('TEST_ENV') == 'False' else os.getenv('TEST_MINIO_BUCKET')
print('MINIO_BUCKET->', MINIO_BUCKET)
storage_handler = MinioHandler(
    os.getenv('MINIO_URL'),
    os.getenv('MINIO_ACCESS_KEY'),
    os.getenv('MINIO_SECRET_KEY'),
    MINIO_BUCKET,
    False
)


@app.post('/images')
async def upload_image(request: Request):
    async with request.form() as form:
        filename = form['file'].filename
        size = form['file'].size
        contents = form['file'].file
        result = storage_handler.upload_file(filename, contents, size)
        return result


@app.get('/images')
async def list_images():
    return storage_handler.list()


@app.get('/images/{filename}')
async def get_link(filename: str):
    link = storage_handler.get_link(filename)
    return link


@app.delete('/images/{filename}')
async def delete_image(filename: str):
    response = storage_handler.remove_object(filename)
    return response
