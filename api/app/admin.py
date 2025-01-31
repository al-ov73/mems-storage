from .utils.auth_utils import authenticate_user, get_current_user
from sqladmin import ModelView
from .models.user import User
from .models.comment import Comment
from .models.label import Label
from .models.like import Like
from .models.message import Message
from .models.meme import Meme
from .models.visit import Visit
from .config.db_config import db
from sqladmin.authentication import AuthenticationBackend
from fastapi import Request
from typing import Annotated, Optional
from fastapi import Depends, HTTPException, status, UploadFile
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form.get("username"), form.get("password")
        user = authenticate_user(username, password, db)
        if user and user.is_admin:
            return True
        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, token: Annotated[str, Depends(oauth2_scheme)]) -> bool:
        # user = await get_current_user(token)
        # print('user', user)
        # if not token:
        #     return False

        # Check the token in depth
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