from ..schemas.stat import MemesDayStatSchema, VisitsDayStatSchema


async def format_memes_day_stat(stat: list[MemesDayStatSchema]) -> str:
    result = []
    for day in stat:
        day_stat = f"{day.date.strftime('%d %b')}, добавлено: {day.count} шт.\n"
        result.append(day_stat)
    return "".join(result)


def format_visits_day_stat(stat: list[VisitsDayStatSchema]) -> str:
    result = []
    for day in stat:
        day_stat = f"{day.date.strftime('%d %b')}, всего: {day.total} чел., старых: {day.old_users} чел.\n"
        result.append(day_stat)
    return "".join(result)
