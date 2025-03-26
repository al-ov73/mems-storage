from dataclasses import dataclass


@dataclass
class Remainder:
    user_id: int
    task_id: int
    type: str
    is_even: bool
    month_day: str
    week_day: str
    hour: str
    minutes: str
    text: str

    def __post_init__(self):
        if self.minutes == "0":
            self.minutes = "00"

    def __repr__(self):
        match self.type:
            case "daily":
                return f"Ежедневно в {self.hour}:{self.minutes}, '{self.text}'"

            case "two_weeks":
                week_days = {
                    "ПН": "Каждый 2 понедельник",
                    "ВТ": "Каждый 2 вторник",
                    "СР": "Каждую 2 среду",
                    "ЧТ": "Каждый 2 четверг",
                    "ПТ": "Каждую 2 пятницу",
                    "СБ": "Каждую 2 субботу",
                    "ВС": "Каждое 2 воскресенье",
                }
                return f"{week_days[self.week_day]} в {self.hour}:{self.minutes} '{self.text}'"

            case "weekly":
                week_days = {
                    "ПН": "Каждый понедельник",
                    "ВТ": "Каждый вторник",
                    "СР": "Каждую среду",
                    "ЧТ": "Каждый четверг",
                    "ПТ": "Каждую пятницу",
                    "СБ": "Каждую субботу",
                    "ВС": "Каждое воскресенье",
                }
                return f"{week_days[self.week_day]} в {self.hour}:{self.minutes} '{self.text}'"
            
            case "monthly":
                return f"Каждое {self.month_day} число в {self.hour}:{self.minutes} '{self.text}'"

            case _:
                return "Неизвестный тип"
