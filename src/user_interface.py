import os
from dotenv import load_dotenv
from sorted_by_salary import VacancyManager


def interface():
    load_dotenv()
    base_url = os.getenv("BASE_URL")

    manager = VacancyManager(base_url)
    query = input("Введите название вакансии: ")
    keyword = input("Введите ключевое слово для фильтрации вакансий по описанию: ").strip()
    salary = int(input("Введите желаемую зарплату: "))
    period = int(input("Введите период (в днях): "))
    top_n = int(input("Введите количество топ вакансий для отображения: "))

    print("_____________")
    print()
    manager.fetch_vacancies(query, salary, period)
    manager.display_filtered_vacancies(keyword)
    manager.sort_vacancies_by_salary()
    manager.top_vacancies(top_n)


if __name__ == "__main__":

    interface()
