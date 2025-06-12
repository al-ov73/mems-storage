from sqlalchemy import case, func
from sqlalchemy.orm import Session

from ..models.visit import Visit
from ..schemas.stat import VisitsDayStatSchema
from ..schemas.visit import VisitSchema


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
    async def get_visit_count_by_day(db: Session, limit: int = 5) -> list[VisitsDayStatSchema]:
        """
        return list of visits from db
        """
        visits = (
            db.query(
                func.date(Visit.visit_at).label("date"),
                func.count(Visit.id).label("total"),
                func.sum(case((Visit.is_new_user == True, 1), else_=0)).label("new_users"),
                func.sum(case((Visit.is_new_user == False, 1), else_=0)).label("old_users"),
            )
            .group_by(func.date(Visit.visit_at))
            .order_by(func.date(Visit.visit_at).desc())
            .limit(limit)
            .all()
        )
        return visits

    @staticmethod
    async def get_last_visits(db: Session, limit: int = 10):
        """
        return list of visits from db with visit count per IP
        """
        subquery = (
            db.query(
                Visit.ip,
                func.count(Visit.id).label('visit_count')
            )
            .group_by(Visit.ip)
            .subquery()
        )

        visits = (
            db.query(
                Visit,
                subquery.c.visit_count
            )
            .join(subquery, Visit.ip == subquery.c.ip)
            .order_by(Visit.visit_at.desc())
            .limit(limit)
            .all()
        )

        result = []
        for visit, count in visits:
            visit.visit_count = count
            result.append(visit)

        return result

    @staticmethod
    async def get_old_users(
        db: Session,
    ) -> int:
        """
        return list of visits with  from db
        """
        old_visits = db.query(Visit).filter_by(is_new_user=False).count()
        return old_visits
