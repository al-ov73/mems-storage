# https://habr.com/ru/companies/otus/articles/801253/

import datetime
import os
import io
# import jwt
from typing import Annotated

# from dateutil.relativedelta import relativedelta

from fastapi import FastAPI, UploadFile, File, Form, Request
from starlette.responses import StreamingResponse, JSONResponse
from .handler import MinioHandler
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
 
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
        return storage_handler.upload_file(filename, contents, size)


@app.get('/list')
async def list_files():
    return storage_handler.list()


# @app.get('/link/{file}')
# async def link(file: str):
#     obj = storage_handler.stats(file)
#     payload = {
#         "filename": obj.object_name,
#         "valid_til": str(datetime.datetime.utcnow() + relativedelta(minutes=int(os.getenv('LINK_VALID_MINUTES', 10))))
#     }
#     encoded_jwt = jwt.encode(payload, os.getenv('JWT_SECRET'), algorithm="HS256")

#     return {
#         "link": f"/download/{encoded_jwt}"
#     }


# @app.get('/download/{temp_link}')
# async def download(temp_link: str):
#     try:
#         decoded_jwt = jwt.decode(temp_link, os.getenv('JWT_SECRET'), algorithms=["HS256"])
#     except:
#         return JSONResponse({
#             "status": "failed",
#             "reason": "Link expired or invalid"
#         }, status_code=400)

#     valid_til = datetime.datetime.strptime(decoded_jwt['valid_til'], '%Y-%m-%d %H:%M:%S.%f')
#     if valid_til > datetime.datetime.utcnow():
#         filename = decoded_jwt['filename']
#         return StreamingResponse(
#             storage_handler.download_file(filename),
#             media_type='application/octet-stream'
#         )
#     return JSONResponse({
#         "status": "failed",
#         "reason": "Link expired or invalid"
#     }, status_code=400)