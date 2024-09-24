from typing import Annotated
from fastapi import Depends, UploadFile, File, Form, APIRouter
from sqlalchemy import text
from sqlalchemy.orm import Session

from ..config.db_config import get_db
from ..config.dependencies import get_users_repository
from ..repositories.comments_repository import CommentsRepository
from ..repositories.users_repository import UsersRepository
from ..schemas.memes import MemeDbSchema
from ..schemas.users import UserDbSchema
from ..utils.auth_utils import get_current_user

router = APIRouter()


@router.get(
    '/{user_id}',
    # dependencies=[Depends(get_current_user)],
)
async def get_user_by_id(
    user_id: str,
    db: Session = Depends(get_db),
    users_repo: UsersRepository = Depends(get_users_repository),                
):
    """
    return user from db
    """
    user = await users_repo.get_user(user_id, db)
    return user