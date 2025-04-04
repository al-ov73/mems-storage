if __name__ == "__main__":
    vacancies = search_vacancies(54.369128, 48.686482, "инженер")
    for vacancy in vacancies:
        print(f"{vacancy.name} - {vacancy.employer.get('name', 'Не указано')} {vacancy.salary} - {vacancy.url}")
