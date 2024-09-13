from tempfile import SpooledTemporaryFile


class FakeStorageRepository():
    '''
    override storage repository to not send
    requests to s3 storage
    '''
    def __init__(self, api_url):
        self.api_url = api_url

    async def get_link(self, image_name: str) -> str:
        return 'some_link'

    async def add_image(
        self,
        filename: str,
        file: SpooledTemporaryFile
    ) -> str:
        return filename

    async def delete_image(self, image_name: str) -> str:
        return image_name

    async def update_image(
        self,
        old_name: str,
        new_name: str,
        new_file: SpooledTemporaryFile
    ) -> str:
        return new_name
