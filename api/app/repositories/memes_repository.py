from ..models.like import Like
from ..models.meme import Meme
from ..models.comment import Comment
from ..schemas.memes import MemeDbSchema
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload, selectinload, contains_eager, load_only


class MemesRepository:

    async def get_memes(
        self,
        skip: int,
        limit: int,
        db: Session,
    ) -> list[MemeDbSchema]:
        """
        return list of memes from db
        """

        memes = (
            db.query(Meme)
            .outerjoin(Comment)
            .options(selectinload(Meme.meme_labels))
            # .options(contains_eager(Meme.comments))
            .options(joinedload(Meme.author))
            .options(selectinload(Meme.likes))
            .order_by(Meme.id.desc())
            # .order_by(Comment.id.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        return memes

    async def get_meme(
        self,
        meme_id: str,
        db: Session,
    ) -> MemeDbSchema:
        """
        return meme from db
        """
        meme = (
            db.query(Meme)
            .outerjoin(Comment)
            .options(selectinload(Meme.meme_labels))
            .options(contains_eager(Meme.comments))
            .options(joinedload(Meme.author))
            .options(selectinload(Meme.likes))
            .order_by(Comment.id.desc())
            .filter(Meme.id == meme_id)
            .first()
        )
        if not meme:
            return "meme not exist"
        return meme

    async def add_meme(
        self,
        new_meme: MemeDbSchema,
        db: Session,
    ) -> MemeDbSchema:
        """
        add meme to db
        """
        db.add(new_meme)
        db.commit()
        db.refresh(new_meme)
        return new_meme

    async def del_meme(
        self,
        meme_id: str,
        db: Session,
    ) -> MemeDbSchema:
        """
        delete meme from db
        """
        meme = db.get(Meme, meme_id)
        db.delete(meme)
        db.commit()
        return meme

    async def update_name(
        self,
        meme_id: str,
        filename: str,
        db: Session,
    ) -> MemeDbSchema:
        """
        update meme in db
        """
        try:
            meme = db.get(Meme, meme_id)
            if meme.name != filename:
                meme.name = filename
            db.commit()
            return meme
        except Exception:
            return f'error "{Exception}"'

    async def get_top_liked_memes(
            self,
            limit: int,
            db: Session,
        ) -> list[MemeDbSchema]:
            """
            return list of top liked memes from db
            """

            memes = (
                db.query(
                    Meme.id,
                    Meme.name,
                    func.count(Like.id).label('likes_count')
                    # func.count(Meme.likes)
                )
                .join(Like)
                # .options(selectinload(Meme.likes))
                .group_by(Meme.id, Meme.name)
                .order_by(func.count(Like.id).desc())
                # .options(load_only(Meme.id, Meme.name))
                .limit(limit)
                .all()
            )
            return memes
