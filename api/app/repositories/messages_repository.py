from sqlalchemy.orm import Session, joinedload


from ..models.message import Message
from ..schemas.messages import MessageSchema


class MessagesRepository:

    async def get_messages(
        self,
        skip: int,
        limit: int,
        db: Session,
    ) -> list[MessageSchema]:
        '''
        return list of messages from db
        '''
        query = db.query(Message)
        query = query.options(joinedload(Message.author))
        return query

    async def get_message(
            self,
            message_id: str,
            db: Session,
    ) -> MessageSchema:
        '''
        return message from db
        '''
        message = db.get(Message, message_id)
        if not message:
            return 'message not exist'
        return message

    async def add_message(
            self,
            new_message: MessageSchema,
            db: Session,
    ) -> MessageSchema:
        '''
        add message to db
        '''
        db.add(new_message)
        db.commit()
        db.refresh(new_message)
        return new_message
