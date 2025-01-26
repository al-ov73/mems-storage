from sqlalchemy.orm import Session

from ..models.visit import Visit
from ..schemas.visit import VisitInputSchema, VisitSchema


class VisitRepository:

    @staticmethod
    async def add_visit(
        new_visit: Visit,
        db: Session,
        commit: bool = True,
    ) -> VisitSchema:
        """
        add visit to db
        """
        db.add(new_visit)
        if commit:
            db.commit()
            db.refresh(new_visit)
        return new_visit
