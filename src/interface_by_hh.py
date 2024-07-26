import os
from dotenv import load_dotenv
from src.vacancy_manager import VacancyManager
import logging


logger = logging.getLogger(__name__)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path = os.path.join(BASE_DIR, "logs", "interface_by_hh.log")
file_handler = logging.FileHandler(path, encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


def interface_hh():
    load_dotenv()
    base_url = os.getenv("BASE_URL")

    manager = VacancyManager(base_url)

    while True:
        query = input("Введите название вакансии: ").strip()
        if not query:
            print("Ошибка: Название вакансии не может быть пустым. Пожалуйста, введите корректное значение.")
        else:
            break

    keyword = input("Введите ключевое слово для фильтрации вакансий по описанию (или оставьте пустым): ").strip()

    while True:
        salary_input = input("Введите числом желаемую зарплату: ")
        if not salary_input.isdigit():
            print("Ошибка: Зарплата должна быть числом. Пожалуйста, введите корректное значение.")
        else:
            salary = int(salary_input)
            break

    while True:
        period_input = input("Введите период (в днях): ")
        if not period_input.isdigit():
            print("Ошибка: Период должен быть числом. Пожалуйста, введите корректное значение.")
        else:
            period = int(period_input)
            break

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
