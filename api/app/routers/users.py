from typing import Annotated
from fastapi import Depends, UploadFile, File, Form, APIRouter
from sqlalchemy import text
from sqlalchemy.orm import Session

from ..config.db_config import get_db
from ..config.dependencies import get_storage_repo, get_users_repository
from ..config.logger_config import get_logger
from ..repositories.comments_repository import CommentsRepository
from ..repositories.storage_repository import BaseStorageRepo
from ..repositories.users_repository import UsersRepository
from ..schemas.memes import MemeDbSchema
from ..schemas.users import UserDbSchema, UserWithPhoto
from ..utils.auth_utils import get_current_user

router = APIRouter()

logger = get_logger(__name__)

@router.get(
    '/{user_id}',
    # dependencies=[Depends(get_current_user)],
)
async def get_user_by_id(
    user_id: str,
    db: Session = Depends(get_db),
    users_repo: UsersRepository = Depends(get_users_repository),
    storage_repo: BaseStorageRepo = Depends(get_storage_repo),             
) -> UserWithPhoto:
    """
    return user from db
    """
    user = await users_repo.get_user(user_id, db)
    storage_username = f'user_{user.username}'
    logger.debug(f'get username {storage_username}')
    link = await storage_repo.get_link(storage_username)
    logger.debug(f'get link {link}')
    user.photo = link
    return user