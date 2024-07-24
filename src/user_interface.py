import os
from dotenv import load_dotenv
from sorted_by_salary import VacancyManager


def interface():
    load_dotenv()
    base_url = os.getenv("BASE_URL")

    manager = VacancyManager(base_url)
    query = input("Введите название вакансии: ")
    salary = int(input("Введите желаемую зарплату: "))
    period = int(input("Введите период (в днях): "))

    manager.fetch_vacancies(query, salary, period)
    manager.sort_vacancies_by_salary()
    manager.display_vacancies()


if __name__ == "__main__":

    interface()
