from ..models.models import Message
from ..schemas.messages import MessageSchema
from sqlalchemy.orm import Session


class MessagesRepository:

    async def get_messages(
            self,
            db: Session,
    ) -> list[MessageSchema]:
        '''
        return list of messages from db
        '''
        messages = db.query(Message).all()
        return messages

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