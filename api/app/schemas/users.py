from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    username: str


class UserDbSchema(UserSchema):
    hashed_password: str
