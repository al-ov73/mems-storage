from pydantic import BaseModel


class LikeSchema(BaseModel):
    id: int
    author_id: int
    meme_id: int
