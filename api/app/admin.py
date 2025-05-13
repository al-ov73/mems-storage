from datetime import timedelta
from typing import Annotated

from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer
from sqladmin import ModelView
from sqladmin.authentication import AuthenticationBackend

from .config.config import ACCESS_TOKEN_EXPIRE_MINUTES
from .config.db_config import db
from .models.comment import Comment
from .models.label import Label
from .models.like import Like
from .models.meme import Meme
from .models.message import Message
from .models.user import User
from .models.visit import Visit
from .utils.auth_utils import authenticate_user, create_access_token, get_current_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form.get("username"), form.get("password")
        user = authenticate_user(username, password, db)
        if user and user.is_admin:
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(user=user, expires_delta=access_token_expires)
            request.session.update({"token": access_token})
            print("access_token", access_token)
            return True
        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        if not token:
            return False

        return True


class UserAdmin(ModelView, model=User):
    column_list = "__all__"


class CommentAdmin(ModelView, model=Comment):
    column_list = "__all__"


class LabelAdmin(ModelView, model=Label):
    column_list = "__all__"


class LikeAdmin(ModelView, model=Like):
    column_list = "__all__"


class MessageAdmin(ModelView, model=Message):
    column_list = "__all__"


class MemeAdmin(ModelView, model=Meme):
    column_list = "__all__"


class VisitAdmin(ModelView, model=Visit):
    column_list = "__all__"


admin_views = [
    UserAdmin,
    CommentAdmin,
    LabelAdmin,
    LikeAdmin,
    MessageAdmin,
    MemeAdmin,
    VisitAdmin,
]
