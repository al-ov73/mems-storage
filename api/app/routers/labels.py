from fastapi import Depends, Form, APIRouter
from sqlalchemy.orm import Session

from ..config.db_config import get_db
from ..config.dependencies import (
    get_labels_repository,
    get_memes_repository,
)
from ..repositories.memes_repository import MemesRepository
from ..repositories.labels_repository import LabelsRepository
from ..schemas.memes import MemeDbSchema
from ..utils.auth_utils import get_current_user

router = APIRouter()


@router.get(
    "",
    dependencies=[Depends(get_current_user)],
)
async def get_labels(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    labels_repo: LabelsRepository = Depends(get_labels_repository),
):
    """
    return list of labels
    """
    labels = await labels_repo.get_labels(skip, limit, db)
    return labels


@router.post("")
async def post_label(
    title: str = Form(),
    meme_id: str = Form(),
    db: Session = Depends(get_db),
    labels_repo: LabelsRepository = Depends(get_labels_repository),
    meme_repo: MemesRepository = Depends(get_memes_repository),
    # user: UserDbSchema = Depends(get_current_user),
) -> MemeDbSchema:
    """
    add label to db
    """
    label = await labels_repo.get_label_by_title(title, db)
    if not label:
        label = await labels_repo.add_label(title, db)
    current_meme = await meme_repo.get_meme(meme_id, db)
    current_meme.meme_labels.append(label)
    db.commit()
    return current_meme
