from pydantic import BaseModel


class UserSchema(BaseModel):
    username: str


class UserDbSchema(UserSchema):
    hashed_password: str
