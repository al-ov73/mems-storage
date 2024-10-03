from sqlalchemy.orm import Session

from ..models.like import Like
from ..schemas.likes import LikeSchema


class LikesRepository:

    async def get_likes(
            self,
            db: Session,
    ) -> list[LikeSchema]:
        '''
        return list of likes from db
        '''
        likes = db.query(Like).all()
        return likes

    async def add_like(
            self,
            author_id: int,
            meme_id: int,
            db: Session,
    ) -> LikeSchema:
        '''
        add like to db
        '''
        new_like = Like(
            author_id=author_id,
            meme_id=meme_id,
        )
        db.add(new_like)
        db.commit()
        db.refresh(new_like)
        return new_like

    async def del_like(
            self,
            like_id: str,
            db: Session,
    ) -> LikeSchema:
        '''
        delete like from db
        '''
        like = db.query(Like).filter(Like.id == like_id).first()
        db.delete(like)
        db.commit()
        return like
