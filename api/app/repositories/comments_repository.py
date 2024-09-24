from sqlalchemy.orm import Session

from ..models.comment import Comment
from ..schemas.comments import CommentSchema


class CommentsRepository:

    async def get_comments(
            self,
            db: Session,
    ) -> list[CommentSchema]:
        '''
        return list of all comments from db
        '''
        comments = db.query(Comment).all()
        return comments

    async def get_comments_by_meme(
            self,
            meme_id: str,
            db: Session,
    ) -> list[CommentSchema]:
        '''
        return list of comments from db bu meme_id:str
        '''
        comments = db.query(Comment).filter(Comment.meme_id == meme_id).all()
        return comments

    async def add_comment(
            self,
            text:str,
            author_id: int,
            author_name: str,
            meme_id: int,
            db: Session,
    ) -> CommentSchema:
        '''
        add comment to db
        '''
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