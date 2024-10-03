from fastapi import Depends, Form, APIRouter
from sqlalchemy.orm import Session

from ..config.db_config import get_db
from ..config.dependencies import get_comments_repository, get_memes_repository
from ..repositories.comments_repository import CommentsRepository
from ..repositories.memes_repository import MemesRepository
from ..schemas.memes import MemeDbSchema
from ..schemas.users import UserDbSchema
from ..utils.auth_utils import get_current_user

router = APIRouter()


@router.get(
    "",
    dependencies=[Depends(get_current_user)],
)
async def get_comments(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    comments_repo: CommentsRepository = Depends(get_comments_repository),
):
    """
    return list of all db comments
    """
    comments = await comments_repo.get_comments(skip, limit, db)
    return comments


@router.get(
    "/meme/{meme_id}",
    dependencies=[Depends(get_current_user)],
)
async def get_comments_by_meme_id(
    meme_id: str,
    db: Session = Depends(get_db),
    comments_repo: CommentsRepository = Depends(get_comments_repository),
):
    """
    return list of meme comments
    """
    comments = await comments_repo.get_comments_by_meme(meme_id, db)
    return comments


@router.post("")
async def post_comment(
    text: str = Form(),
    meme_id: str = Form(),
    db: Session = Depends(get_db),
    comments_repo: CommentsRepository = Depends(get_comments_repository),
    meme_repo: MemesRepository = Depends(get_memes_repository),
    user: UserDbSchema = Depends(get_current_user),
) -> MemeDbSchema:
    """
    add comment to db
    """
    author_id = user.id
    author_username = user.username
    new_comment = await comments_repo.add_comment(
        text, author_id, author_username, meme_id, db
    )
    current_meme = await meme_repo.get_meme(meme_id, db)
    current_meme.comments.append(new_comment)
    db.commit()
    return current_meme
