from datetime import datetime, timedelta

from sqlalchemy import func
from sqlalchemy.orm import Session, contains_eager, selectinload

from ..models.comment import Comment
from ..models.label import LabelMeme
from ..models.like import Like
from ..models.meme import Meme
from ..schemas.memes import MemeDbSchema
from ..schemas.stat import MemesDayStatSchema, SourceStatSchema, StatSchema


class MemesRepository:

    @staticmethod
    async def get_memes(
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
            .options(contains_eager(Meme.comments))
            .options(selectinload(Meme.likes))
            .order_by(Meme.id.desc())
            .order_by(Comment.id.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        return memes

    @staticmethod
    async def get_checked_memes(
        skip: int,
        limit: int,
        db: Session,
    ) -> list[MemeDbSchema]:
        """
        return list of checked memes from db
        """
        memes = (
            db.query(Meme)
            .filter_by(checked=True)
            .outerjoin(Comment)
            .options(selectinload(Meme.meme_labels))
            .options(contains_eager(Meme.comments))
            .options(selectinload(Meme.likes))
            .order_by(Meme.id.desc())
            .order_by(Comment.id.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        return memes

    @staticmethod
    async def get_meme_names(
        db: Session,
    ) -> list[str]:
        """
        Return list of only meme names from db
        """
        memes = db.query(Meme.name).filter_by(checked=True).order_by(Meme.id.desc()).all()
        return [meme[0] for meme in memes]

    @staticmethod
    async def get_not_checked_memes(
        skip: int,
        limit: int,
        db: Session,
    ) -> list[MemeDbSchema]:
        """
        return list of not checked memes from db
        """
        memes = (
            db.query(Meme)
            .filter_by(checked=False)
            .outerjoin(Comment)
            .options(selectinload(Meme.meme_labels))
            .options(contains_eager(Meme.comments))
            .options(selectinload(Meme.likes))
            .order_by(Meme.id.desc())
            .order_by(Comment.id.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        return memes

    @staticmethod
    async def get_random_meme(
        db: Session,
    ) -> MemeDbSchema:
        """
        return random memes from db
        """
        random_meme = db.query(Meme).filter_by(published=False).filter_by(checked=True).order_by(func.random()).first()
        return random_meme

    @staticmethod
    async def get_published_stat(
        db: Session,
    ) -> StatSchema:
        """
        return random memes from db
        """
        total = db.query(Meme).filter_by(checked=True).count()
        published = db.query(Meme).filter_by(checked=True).filter_by(published=True).count()
        not_published = total - published
        not_checked = db.query(Meme).filter_by(checked=False).count()
        return StatSchema(
            total=total,
            published=published,
            not_published=not_published,
            not_checked=not_checked,
        )

    @staticmethod
    async def get_sources_stat(
        db: Session,
        limit: int = 3,
    ) -> list[SourceStatSchema]:
        """
        return sources stat from db
        """
        ago_condition = datetime.now() - timedelta(days=limit)

        memes = (
            db.query(
                Meme.source_name.label("source_name"),
                Meme.source_type.label("source_type"),
                func.count(Meme.id).label("count"),
            )
            .filter(Meme.created_at >= ago_condition)
            .group_by(Meme.source_name, Meme.source_type)
            .order_by(Meme.source_type)
            .all()
        )
        return memes

    @staticmethod
    async def get_meme(
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
            .options(selectinload(Meme.likes))
            .order_by(Comment.id.desc())
            .filter(Meme.id == meme_id)
            .first()
        )
        if not meme:
            return "meme not exist"
        return meme

    @staticmethod
    async def check_memes(
        meme_ids: list[int],
        db: Session,
    ) -> [int]:
        """
        return meme from db
        """
        changed_ids = []
        for meme_id in meme_ids:
            meme = db.query(Meme).filter(Meme.id == meme_id).first()
            if meme:
                meme.checked = True
                db.commit()
                db.refresh(meme)
                changed_ids.append(meme_id)
        return changed_ids

    @staticmethod
    async def add_meme(
        new_meme: MemeDbSchema,
        db: Session,
        commit: bool = True,
    ) -> MemeDbSchema:
        """
        add meme to db
        """
        db.add(new_meme)
        if commit:
            db.commit()
            db.refresh(new_meme)
        return new_meme

    @staticmethod
    async def del_meme(
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

    @staticmethod
    async def make_meme_published(
        meme_id: int,
        db: Session,
    ) -> MemeDbSchema:
        """
        delete meme from db
        """
        meme = db.get(Meme, meme_id)
        meme.published = True
        db.commit()
        return meme

    @staticmethod
    async def update_name(
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

    @staticmethod
    async def get_top_liked_memes(
        limit: int,
        db: Session,
    ) -> list[MemeDbSchema]:
        """
        return list of top liked memes from db
        """
        memes = (
            db.query(Meme.id, Meme.name, func.count(Like.id).label("likes_count"))
            .join(Like)
            .group_by(Meme.id, Meme.name)
            .order_by(func.count(Like.id).desc())
            .limit(limit)
            .all()
        )
        return memes

    @staticmethod
    async def get_memes_count_by_day(db: Session, limit: int = 5) -> list[MemesDayStatSchema]:
        """
        return list of top liked memes from db
        """
        memes = (
            db.query(
                func.date(Meme.created_at).label("date"),
                func.count(Meme.id).label("count"),
            )
            .group_by(func.date(Meme.created_at))
            .order_by(func.date(Meme.created_at).label("date").desc())
            .limit(limit)
            .all()
        )
        return memes

    @staticmethod
    async def add_preview_if_not_exist(
        db: Session,
    ) -> list[MemeDbSchema]:
        """
        return list of memes from db
        """
        memes = db.query(Meme).all()
        for meme in memes:
            if not meme.preview:
                preview = meme.link.replace("photos", "previews").replace("jpg", "jpeg")
                meme.preview = preview
        db.commit()
        return memes

    @staticmethod
    async def delete_old_memes(
        db: Session,
        older_then_days: int = 120,
        batch_size: int = 100,
    ) -> list[str]:
        """
        Delete memes older than specified days and return their IDs.
        Handles related data (comments, likes, labels) properly.
        """
        four_months_ago = datetime.now() - timedelta(days=older_then_days)
        deleted_ids = []
        deleted_names = []
        while True:
            old_memes = db.query(Meme).filter(Meme.created_at < four_months_ago).limit(batch_size).all()

            if not old_memes:
                break

            old_memes_ids = [meme.id for meme in old_memes]
            old_memes_names = [meme.name for meme in old_memes]
            deleted_ids.extend(old_memes_ids)
            deleted_names.extend(old_memes_names)
            db.query(Like).filter(Like.meme_id.in_(old_memes_ids)).delete(synchronize_session=False)
            db.query(Comment).filter(Comment.meme_id.in_(old_memes_ids)).delete(synchronize_session=False)
            db.query(LabelMeme).filter(LabelMeme.meme_id.in_(old_memes_ids)).delete(synchronize_session=False)
            db.query(Meme).filter(Meme.id.in_(old_memes_ids)).delete(synchronize_session=False)

            db.commit()

        return deleted_names
