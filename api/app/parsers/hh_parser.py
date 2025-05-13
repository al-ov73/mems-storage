from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import requests

from ..config.config import LEFT_TOP_COORDS, RIGHT_BOTTOM_COORDS, VACANCY_TEXT


@dataclass
class Vacancy:
    id: str
    name: str
    area: Dict[str, Any]
    salary: Optional[Dict[str, Any]]
    employer: Dict[str, Any]
    published_at: str
    url: str


def search_vacancies() -> List[Vacancy]:
    url = "https://api.hh.ru/vacancies"
    params = {
        "text": VACANCY_TEXT,
        "area": 98,  # ID региона Ульяновск
        # "search_field": "name",  # Искать только в названии вакансии
        "per_page": 10,  # Количество вакансий на странице
        "page": 0,
        "order_by": "publication_time",
        "top_lat": LEFT_TOP_COORDS[0],
        "bottom_lat": RIGHT_BOTTOM_COORDS[0],
        "left_lng": LEFT_TOP_COORDS[1],
        "right_lng": RIGHT_BOTTOM_COORDS[1],
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        vacancies = [
            Vacancy(
                id=vacancy.get("id", ""),
                name=vacancy.get("name", ""),
                area=vacancy.get("area", {}),
                salary=vacancy.get("salary"),
                employer=vacancy.get("employer", {}),
                published_at=vacancy.get("published_at", ""),
                url=vacancy.get("alternate_url", ""),
            )
            for vacancy in data.get("items", [])
        ]
        return vacancies
    else:
        print(f"Ошибка: {response.status_code}")
        return []
