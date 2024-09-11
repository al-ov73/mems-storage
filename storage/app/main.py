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
async def upload_image(request: Request):
    async with request.form() as form:
        print('get upload request', form)
        print('file->', form['file'])
        filename = form['file'].filename
        size = form['file'].size
        contents = form['file'].file
        result = storage_handler.upload_file(filename, contents, size)
        print('storage response', result)
        return result


@app.get('/images')
async def list_images():
    return storage_handler.list()


@app.get('/images/link/{filename}')
async def get_link(filename: str):
    link = storage_handler.get_link(filename)
    return link

@app.get('/images/{filename}')
async def get_object(filename: str):
    obj = storage_handler.get_object(filename)
    print('obj', type(obj))
    print('obj.data', type(obj.data))
    return Response(content=obj.data)

@app.delete('/images/{filename}')
async def delete_image(filename: str):
    response = storage_handler.remove_object(filename)
    return response
