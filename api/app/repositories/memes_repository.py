from ..models.models import Meme, CategoryEnum
from ..schemas.memes import MemeDbSchema
from sqlalchemy.orm import Session


class MemesRepository:

    async def get_memes(
            self,
            skip: int,
            limit: int,
            db: Session,
    ) -> list[MemeDbSchema]:
        '''
        return list of memes from db
        '''
        memes = db.query(Meme).offset(skip).limit(limit).all()
        return memes

    async def get_meme(
            self,
            meme_id: str,
            db: Session,
    ) -> MemeDbSchema:
        '''
        return meme from db
        '''
        meme = db.get(Meme, meme_id)
        if not meme:
            return 'meme not exist'
        return meme

    async def add_meme(
            self,
            new_meme: MemeDbSchema,
            db: Session,
    ) -> MemeDbSchema:
        '''
        add meme to db
        '''
        db.add(new_meme)
        db.commit()
        db.refresh(new_meme)
        return new_meme

    async def del_meme(
            self,
            meme_id: str,
            db: Session,
    ) -> MemeDbSchema:
        '''
        delete meme from db
        '''
        try:
            meme = db.get(Meme, meme_id)
            db.delete(meme)
            db.commit()
            return meme
        except Exception:
            return f'error "{Exception}"'

    async def update_name(
            self,
            meme_id: str,
            filename: str,
            db: Session,
    ) -> MemeDbSchema:
        '''
        update meme in db
        '''
        try:
            meme = db.get(Meme, meme_id)
            if meme.name != filename:
                meme.name = filename
            db.commit()
            return meme
        except Exception:
            return f'error "{Exception}"'

