from typing import Annotated
from fastapi import Depends, UploadFile, File, Form, APIRouter
from sqlalchemy import text
from sqlalchemy.orm import Session

from ..config.db_config import get_db
from ..config.dependencies import get_storage_repo, get_memes_labels
from ..models.models import Meme
from ..repositories.memes_repository import MemesRepository
from ..repositories.storage_repository import BaseStorageRepo
from ..repositories.labels_repository import LabelsRepository
from ..schemas.memes import MemeDbSchema, MemeSchema
from ..schemas.users import UserDbSchema
from ..utils.auth_utils import get_current_user

router = APIRouter()


@router.get(
    '',
    dependencies=[Depends(get_current_user)],
)
async def get_labels(skip: int = 0,
                    limit: int = 100,
                    db: Session = Depends(get_db),
                    labels_repo: LabelsRepository = Depends(get_labels_repository),
                    ):
    """
    return list of labels
    """
    labels = await labels_repo.get_labels(skip, limit, db)
    return labels

