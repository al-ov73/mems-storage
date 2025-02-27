from dataclasses import dataclass

@dataclass
class Remainder:
    user_id: int
    task_id: int
    type: str
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
            case 'dayly':
                return f"Ежедневно в {self.hour}:{self.minutes}, '{self.text}'"

            case 'weekly':
                week_days = {
                    "ПН": "Каждый понедельник",
                    "ВТ": "Каждый вторник",
                    "СР": "Каждую среду",
                    "ЧТ": "Каждый четверг",
                    "ПТ": "Каждую пятницу",
                    "СБ": "Каждую субботу",
                    "ВС": "Каждое воскресенье"
                }
                return f"{week_days[self.week_day]} в {self.hour}:{self.minutes} '{self.text}'"

            case 'monthly':
                return f"Каждое {self.month_day} число в {self.hour}:{self.minutes} '{self.text}'"

            case _:
                pass
