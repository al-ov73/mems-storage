from ..models.label import Label
from ..schemas.labels import LabelSchema
from sqlalchemy.orm import Session


class LabelsRepository:

    async def get_labels(
            self,
            skip: int,
            limit: int,
            db: Session,
    ) -> list[LabelSchema]:
        '''
        return list of labels from db
        '''
        labels = db.query(Label).offset(skip).limit(limit).all()
        return labels

    async def get_label_by_title(
            self,
            label_title: str,
            db: Session,
    ) -> list[LabelSchema]:
        '''
        return label by title from db
        '''
        label = db.query(Label).filter(Label.title == label_title).first()
        return label

    async def add_label(
            self,
            label_title: str,
            db: Session,
    ) -> LabelSchema:
        '''
        add label to db
        '''
        new_label = Label(title=label_title)
        db.add(new_label)
        db.commit()
        db.refresh(new_label)
        return new_label
