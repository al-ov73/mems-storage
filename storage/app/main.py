import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response
from urllib3 import HTTPResponse

from .handlers.minio_handler import MinioHandler

load_dotenv()

app = FastAPI()

storage_handler = MinioHandler(
    os.getenv('MINIO_URL'),
    os.getenv('MINIO_ACCESS_KEY'),
    os.getenv('MINIO_SECRET_KEY'),
    os.getenv('MINIO_BUCKET'),
    False
)

@app.post('/images')
async def upload_image(request: Request) -> Response:
    async with request.form() as form:
        filename = form['file'].filename
        size = form['file'].size
        contents = form['file'].file
        result = storage_handler.upload_file(filename, contents, size)
        return Response(content=result)

@app.get('/images')
async def list_images() -> Response:
    images_list = storage_handler.list()
    return Response(content=images_list)

@app.get('/images/link/{filename}')
async def get_link(filename: str) -> Response:
    link = storage_handler.get_link(filename)
    return Response(content=link)

@app.get('/images/{filename}')
async def get_object(filename: str) -> Response:
    obj = storage_handler.get_object(filename)
    return Response(content=obj)

@app.delete('/images/{filename}')
async def delete_image(filename: str) -> Response:
    response = storage_handler.remove_object(filename)
    return Response(content=response)
