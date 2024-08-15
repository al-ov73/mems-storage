from datetime import datetime
from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None

class User(BaseModel):
    username: str


class UserInDB(User):
    hashed_password: str

class Meme(BaseModel):
    id: int
    name: str
    created_at: datetime
    link: str


class MemeWithLink(Meme):
    id: int
    name: str
    link: str
    created_at: datetime
