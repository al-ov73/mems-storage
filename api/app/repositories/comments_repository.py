from sqlalchemy.orm import Session

from ..models.models import Comment
from ..schemas.comments import CommentSchema


class CommentsRepository:

    async def get_comments(
            self,
            db: Session,
    ) -> list[CommentSchema]:
        '''
        return list of comments from db
        '''
        comments = db.query(Comment).all()
        return comments

    async def add_comment(
            self,
            text:str,
            author_id: int,
            meme_id: int,
            db: Session,
    ) -> CommentSchema:
        '''
        add comment to db
        '''
        new_comment = Comment(
            text=text,
            author_id=author_id,
            meme_id=meme_id
        )
        db.add(new_comment)
        db.commit()
        db.refresh(new_comment)
        return new_comment