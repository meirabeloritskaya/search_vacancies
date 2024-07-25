import os
from dotenv import load_dotenv
from src.vacancy_manager import VacancyManager


def interface_hh():
    load_dotenv()
    base_url = os.getenv("BASE_URL")

    manager = VacancyManager(base_url)

    query = input("Введите название вакансии: ")
    keyword = input("Введите ключевое слово для фильтрации вакансий по описанию: ").strip()
    salary = int(input("Введите желаемую зарплату: "))
    period = int(input("Введите период (в днях): "))

    print("_____________")
    print()
    manager.fetch_vacancies(query, salary, period)
    vacancies_hh = manager.display_filtered_vacancies(keyword)

    return vacancies_hh


if __name__ == "__main__":
    vacancies = interface_hh()
    if vacancies:  # Проверяем, что список не пустой и не None
        for vacancy in vacancies:
            print(vacancy)
            print()
    else:
        print("Нет вакансий для отображения.")
