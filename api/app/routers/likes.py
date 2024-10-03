from fastapi import Depends, Form, APIRouter
from sqlalchemy.orm import Session

from ..config.db_config import get_db
from ..config.dependencies import get_likes_repository, get_memes_repository
from ..repositories.likes_repository import LikesRepository
from ..repositories.memes_repository import MemesRepository
from ..schemas.memes import MemeDbSchema
from ..schemas.users import UserDbSchema
from ..schemas.likes import LikeSchema
from ..utils.auth_utils import get_current_user


router = APIRouter()


@router.get(
    "",
    dependencies=[Depends(get_current_user)],
)
async def get_likes(
    db: Session = Depends(get_db),
    likes_repo: LikesRepository = Depends(get_likes_repository),
):
    """
    return list of likes
    """
    likes = await likes_repo.get_likes(db)
    return likes


@router.post("")
async def post_like(
    meme_id: str = Form(),
    db: Session = Depends(get_db),
    likes_repo: LikesRepository = Depends(get_likes_repository),
    meme_repo: MemesRepository = Depends(get_memes_repository),
    user: UserDbSchema = Depends(get_current_user),
) -> MemeDbSchema:
    """
    add like to db
    """
    author_id = user.id
    new_like = await likes_repo.add_like(author_id, meme_id, db)
    current_meme = await meme_repo.get_meme(meme_id, db)
    current_meme.likes.append(new_like)
    db.commit()
    return current_meme


@router.delete(
    "/{like_id}",
)
async def delete_like(
    like_id: str,
    db: Session = Depends(get_db),
    likes_repo: LikesRepository = Depends(get_likes_repository),
) -> LikeSchema:
    """
    add like to db
    """
    like = await likes_repo.del_like(like_id, db)
    return like
