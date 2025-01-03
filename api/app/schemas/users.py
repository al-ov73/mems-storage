from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    username: str
    first_name: str | None
    last_name: str | None
    is_admin: bool


class UserDbSchema(UserSchema):
    hashed_password: str
