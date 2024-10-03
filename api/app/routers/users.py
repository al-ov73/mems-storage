from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from ..config.db_config import get_db
from ..config.dependencies import get_storage_repo, get_users_repository
from ..config.logger_config import get_logger
from ..repositories.storage_repository import BaseStorageRepo
from ..repositories.users_repository import UsersRepository
from ..schemas.users import UserWithPhoto

router = APIRouter()

logger = get_logger(__name__)


@router.get(
    "/{user_id}",
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
    storage_username = f"user_{user.username}"
    logger.debug(f"get username {storage_username}")
    link = await storage_repo.get_link(storage_username)
    logger.debug(f"get link {link}")
    user.photo = link
    return user
