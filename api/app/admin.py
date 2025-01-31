from sqladmin import ModelView
from .models.user import User
from .models.comment import Comment
from .models.label import Label
from .models.like import Like
from .models.message import Message
from .models.meme import Meme
from .models.visit import Visit

from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]

        print(username, password)

        return True

    async def logout(self, request: Request) -> bool:
        # Usually you'd want to just clear the session
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

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