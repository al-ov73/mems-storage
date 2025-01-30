from ..schemas.stat import DayStatSchema


async def format_day_stat(stat: list[DayStatSchema], title: str) -> str:
    result = []
    for day in stat:
        day_stat = f"{day.date.strftime("%d %b")}, {title}: {day.count} шт.\n"
        result.append(day_stat)
    return "".join(result)
