import minio

from minio import Minio
from typing import BinaryIO
from urllib3.response import HTTPResponse


class MinioHandler:
    def __init__(self, minio_endpoint: str, access_key: str, secret_key: str,
                 bucket: str, secure: bool = False):
        self.client = Minio(
            minio_endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure
        )
        self.bucket = bucket

    def upload_file(self, filename: str, file: BinaryIO, length: int) -> str:
        self.client.put_object(self.bucket, filename, file, length=length,
                                      content_type='image/jpeg')
        return f'object {filename} uploded'

    def list(self) -> list:
        objects = list(self.client.list_objects(self.bucket))
        return [{"name": i.object_name, "last_modified": i.last_modified} for i
                in objects]

    def stats(self, name: str) -> minio.api.Object:
        return self.client.stat_object(self.bucket, name)

    def get_object(self, filename: str) -> HTTPResponse:
        obj = self.client.get_object(self.bucket, filename)
        return obj.data

    def get_link(self, filename: str) -> str:
        return self.client.get_presigned_url("GET", self.bucket, filename)

    def remove_object(self, filename: str) -> str:
        self.client.remove_object(self.bucket, filename)
        return f'object {filename} removed'
