from ..models.models import Label
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
