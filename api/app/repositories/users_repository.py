from sqlalchemy.orm import Session

from ..models.user import User
from ..schemas.users import UserSchema


class UsersRepository:

    async def get_user(
            self,
            user_id: str,
            db: Session,
    ) -> UserSchema:
        '''
        return user from db
        '''
        user = db.get(User, user_id)
        return user
