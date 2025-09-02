from sqlalchemy import case, func, extract
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional

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
    async def get_visit_count_by_day(db: Session, limit: int = 5, landing_page: Optional[str] = None) -> list[
        VisitsDayStatSchema]:
        """
        return list of visits from db
        """
        query = db.query(
            func.date(Visit.visit_at).label("date"),
            func.count(Visit.id).label("total"),
            func.sum(case((Visit.is_new_user == True, 1), else_=0)).label("new_users"),
            func.sum(case((Visit.is_new_user == False, 1), else_=0)).label("old_users"),
        )

        # Фильтруем по landing_page: если не передан - только "memovoz.ru", если передан - по значению
        if landing_page is None:
            query = query.filter(Visit.landing_page == "memovoz.ru")
        else:
            query = query.filter(Visit.landing_page == landing_page)

        visits = (
            query
            .group_by(func.date(Visit.visit_at))
            .order_by(func.date(Visit.visit_at).desc())
            .limit(limit)
            .all()
        )
        return visits

    @staticmethod
    async def get_last_visits(db: Session, limit: int = 10, landing_page: Optional[str] = None):
        """
        return list of visits from db with visit count per IP
        """
        # Создаем подзапрос с фильтром по landing_page
        subquery = (
            db.query(
                Visit.ip,
                func.count(Visit.id).label('visit_count')
            )
        )
        # Фильтруем подзапрос
        if landing_page is None:
            subquery = subquery.filter(Visit.landing_page == "memovoz.ru")
        else:
            subquery = subquery.filter(Visit.landing_page == landing_page)

        subquery = subquery.group_by(Visit.ip).subquery()

        # Основной запрос
        main_query = (
            db.query(
                Visit,
                subquery.c.visit_count
            )
            .join(subquery, Visit.ip == subquery.c.ip)
        )

        # Фильтруем основной запрос
        if landing_page is None:
            main_query = main_query.filter(Visit.landing_page == "memovoz.ru")
        else:
            main_query = main_query.filter(Visit.landing_page == landing_page)

        visits = (
            main_query
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
    async def get_old_users(db: Session, landing_page: Optional[str] = None) -> int:
        """
        return count of old users
        """
        query = db.query(Visit).filter_by(is_new_user=False)

        # Фильтруем по landing_page
        if landing_page is None:
            query = query.filter(Visit.landing_page == "memovoz.ru")
        else:
            query = query.filter(Visit.landing_page == landing_page)

        old_visits = query.count()
        return old_visits

    @staticmethod
    async def get_weekly_visits_stats(db: Session, weeks: int = 8, landing_page: Optional[str] = None) -> str:
        """
        Получить статистику визитов по неделям
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(weeks=weeks)

        query = db.query(
            func.date_trunc('week', Visit.visit_at).label('week_start'),
            func.count(Visit.id).label('total_visits'),
            func.count(func.distinct(Visit.ip)).label('unique_users')
        ).filter(Visit.visit_at >= start_date)

        # Фильтруем по landing_page
        if landing_page is None:
            query = query.filter(Visit.landing_page == "memovoz.ru")
        else:
            query = query.filter(Visit.landing_page == landing_page)

        weekly_stats = (
            query
            .group_by(func.date_trunc('week', Visit.visit_at))
            .order_by(func.date_trunc('week', Visit.visit_at).desc())
            .all()
        )

        result = []
        for stat in weekly_stats:
            week_start = stat.week_start
            week_end = week_start + timedelta(days=6)

            formatted_stat = VisitRepository._format_weekly_stat(
                week_start, week_end, stat.total_visits, stat.unique_users
            )
            result.append(formatted_stat)

        return "\n".join(result)

    @staticmethod
    async def get_monthly_visits_stats(db: Session, months: int = 6, landing_page: Optional[str] = None) -> str:
        """
        Получить статистику визитов по месяцам
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=months * 30)

        query = db.query(
            func.date_trunc('month', Visit.visit_at).label('month_start'),
            func.count(Visit.id).label('total_visits'),
            func.count(func.distinct(Visit.ip)).label('unique_users')
        ).filter(Visit.visit_at >= start_date)

        # Фильтруем по landing_page
        if landing_page is None:
            query = query.filter(Visit.landing_page == "memovoz.ru")
        else:
            query = query.filter(Visit.landing_page == landing_page)

        monthly_stats = (
            query
            .group_by(func.date_trunc('month', Visit.visit_at))
            .order_by(func.date_trunc('month', Visit.visit_at).desc())
            .all()
        )

        result = []
        for stat in monthly_stats:
            formatted_stat = VisitRepository._format_monthly_stat(
                stat.month_start, stat.total_visits, stat.unique_users
            )
            result.append(formatted_stat)

        return "\n".join(result)

    # Вспомогательные методы для форматирования

    @staticmethod
    def _format_dates_range(start_date: datetime, end_date: datetime) -> str:
        """
        Форматирует диапазон дат в формате 'дд.мм - дд.мм'
        """
        return f"{start_date.strftime('%d.%m')} - {end_date.strftime('%d.%m')}"

    @staticmethod
    def _format_visits_word(count: int) -> str:
        """
        Правильно склоняет слово 'визит' в зависимости от числа
        """
        if count % 10 == 1 and count % 100 != 11:
            return "визит"
        elif count % 10 in [2, 3, 4] and count % 100 not in [12, 13, 14]:
            return "визита"
        else:
            return "визитов"

    @staticmethod
    def _format_users_word(count: int) -> str:
        """
        Правильно склоняет слово 'пользователь' в зависимости от числа
        """
        if count % 10 == 1 and count % 100 != 11:
            return "пользователь"
        elif count % 10 in [2, 3, 4] and count % 100 not in [12, 13, 14]:
            return "пользователя"
        else:
            return "пользователей"

    @staticmethod
    def _format_weekly_stat(start_date: datetime, end_date: datetime,
                            visits_count: int, users_count: int) -> str:
        """
        Форматирует статистику за неделю в нужный формат
        """
        date_range = VisitRepository._format_dates_range(start_date, end_date)
        visits_word = VisitRepository._format_visits_word(visits_count)
        users_word = VisitRepository._format_users_word(users_count)

        return f"{date_range}: {visits_count} {visits_word}, {users_count} {users_word}"

    @staticmethod
    def _format_month_name(date: datetime) -> str:
        """
        Возвращает название месяца на русском языке
        """
        month_names = {
            1: "январь", 2: "февраль", 3: "март", 4: "апрель",
            5: "май", 6: "июнь", 7: "июль", 8: "август",
            9: "сентябрь", 10: "октябрь", 11: "ноябрь", 12: "декабрь"
        }
        return month_names[date.month]

    @staticmethod
    def _format_monthly_stat(month_date: datetime, visits_count: int, users_count: int) -> str:
        """
        Форматирует статистику за месяц в нужный формат
        """
        month_name = VisitRepository._format_month_name(month_date)
        visits_word = VisitRepository._format_visits_word(visits_count)
        users_word = VisitRepository._format_users_word(users_count)

        return f"{month_name}: {visits_count} {visits_word}, {users_count} {users_word}"