from sqlalchemy.orm import Session
from sqlalchemy import func
from ..models.visit import Visit
from ..schemas.stat import DayStatSchema
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
        exist_visit = db.query(Visit).filter(Visit.ip == new_visit.ip).first()
        new_visit.is_new_user = exist_visit is None
        db.add(new_visit)
        if commit:
            db.commit()
            db.refresh(new_visit)
        return new_visit

    @staticmethod
    async def get_visit_count_by_day(db: Session, limit: int = 5) -> list[DayStatSchema]:
        """
        return list of top liked visits from db
        """
        visits = (
            db.query(
                func.date(Visit.visit_at).label("date"),
                func.count(Visit.id).label("count"),
            )
            .group_by(func.date(Visit.visit_at))
            .order_by(func.date(Visit.visit_at).label("date").desc())
            .limit(limit)
            .all()
        )
        return visits