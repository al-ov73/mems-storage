from api.app.schemas.stat import DayStatSchema


async def format_day_stat(stat: list[DayStatSchema]) -> str:
    result = []
    for day in stat:
        day_stat = f"{day.date.strftime("%d %m")}, добавлено: {day.count} мемов\n"
        result.append(day_stat)
    return "".join(result)
