from sqlalchemy.orm import Session

from ..config.logger_config import get_logger
from ..models.comment import Comment
from ..schemas.comments import CommentSchema

logger = get_logger(__name__)


class CommentsRepository:

    async def get_comments(
        self,
        skip: int,
        limit: int,
        db: Session,
    ) -> list[CommentSchema]:
        """
        return list of all comments from db
        """
        comments = db.query(Comment).all()
        return comments

    async def get_comments_by_meme(
        self,
        meme_id: str,
        db: Session,
    ) -> list[CommentSchema]:
        """
        return list of comments from db bu meme_id:str
        """
        logger.info(f"Request for comments for image id: {meme_id}")
        comments = db.query(Comment).filter(Comment.meme_id == meme_id).all()
        logger.info(f"Received {len(comments)} for image id: {meme_id}")
        return comments

    async def add_comment(
        self,
        text: str,
        author_id: int,
        author_name: str,
        meme_id: int,
        db: Session,
    ) -> CommentSchema:
        """
        add comment to db
        """
        new_comment = Comment(
            text=text,
            author_id=author_id,
            author_name=author_name,
            meme_id=meme_id
        )
        db.add(new_comment)
        db.commit()
        db.refresh(new_comment)
        return new_comment
