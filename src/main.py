import os
from dotenv import load_dotenv
from src.interface_by_hh import interface_hh
from src.interface_by_vacancies_json import JsonVacancyStorage
import json
import logging


logger = logging.getLogger(__name__)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path = os.path.join(BASE_DIR, "logs", "main.log")
file_handler = logging.FileHandler(path, encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


def main():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(BASE_DIR, "data", "vacancies.json")
    load_dotenv()

    storage = JsonVacancyStorage(path)
    with open(path, "r", encoding="utf-8") as file:
        try:
            vacancies = json.load(file)
        except json.JSONDecodeError:
            vacancies = []

    while True:
        action = input(
            "Выберите действие: \n"
            "(0) Выход: \n"
            "(1) Добавить вакансию в json файл\n"
            "(2) Получить вакансии из json файла\n"
            "(3) Вывести сортированный список вакансий\n"
            "(4) Вывести топ-n вакансий\n"
            "(5) Удалить вакансию из json файла\n"
        ).strip()
        if action == "1":
            vacancies = interface_hh()
            for vacancy in vacancies:
                storage.add_vacancy(vacancy)
            print("Вакансии добавлены в файл.")

        elif action == "2":
            # Фильтрация вакансий
            city = input("Введите город для фильтрации (или оставьте пустым): ").strip()
            salary_min = input("Введите минимальную зарплату (или оставьте пустым): ").strip()
            salary_min = int(salary_min) if salary_min else None

            criteria = {}
            if city:
                criteria["city"] = city
            if salary_min is not None:
                criteria["salary"] = salary_min

            filtered_vacancies = storage.get_vacancies(**criteria)
            filtered_vacancies = [
                vacancy for vacancy in filtered_vacancies if not city or vacancy["city"].lower() == city
            ]

            if not filtered_vacancies:
                print("Не найдено вакансий по указанным критериям.")
            else:
                print("Фильтрованные вакансии:")
                for vacancy in filtered_vacancies:
                    print(vacancy)

        elif action == "3":
            # Сортировка вакансий
            while True:

                order = input("Введите порядок сортировки (asc/desc): ").strip().lower()
                if order not in ["asc", "desc"]:
                    print(
                        "Ошибка: Пожалуйста, введите 'asc' для сортировки по возрастанию или 'desc' для сортировки по убыванию."
                    )
                    continue

                if order == "asc":
                    sorted_vacancies_by_salary = storage.sorted_vacancies(False)
                    print("Отсортированные вакансии:")
                    for vacancy in sorted_vacancies_by_salary:
                        print(vacancy)
                    break
                elif order == "desc":
                    sorted_vacancies_by_salary = storage.sorted_vacancies(True)
                    print("Отсортированные вакансии:")
                    for vacancy in sorted_vacancies_by_salary:
                        print(vacancy)
                    break
                else:
                    print(
                        "Ошибка: Пожалуйста, введите 'asc' для сортировки по возрастанию или 'desc' для сортировки по убыванию."
                    )
                    continue

        elif action == "4":

            n = input("Введите количество топ вакансий: ").strip()
            try:
                n = int(n)
                if n <= 0:
                    print("Введите положительное целое число")
                    break
                else:
                    vacancies = storage.sorted_vacancies(True)[:n]
                    for vacansy in vacancies:
                        print(vacansy)
            except ValueError:
                print("Введите положительное целое число")

        elif action == "5":
            while True:
                # Удаление вакансии
                criteria = {}
                criterion = input(
                    "Удалить по городу (введите цифру 1)\n"
                    "Удалить по зарплате (введите цифру 2) \n"
                    "Удалить все вакансии (введите цифру 3): "
                ).strip()
                if criterion == "1":
                    city = input("Введите город для удаления: ").strip().capitalize()
                    criteria["city"] = city
                    rest_vacancies = storage.delete_vacancy(**criteria)
                    for vacancy in rest_vacancies:
                        print(vacancy)
                    break
                elif criterion == "2":
                    salary = input("Введите зарплату для удаления: ").strip()
                    try:
                        criteria["salary"] = int(salary)
                        rest_vacancies = storage.delete_vacancy(**criteria)
                        for vacancy in rest_vacancies:
                            print(vacancy)
                        break
                    except ValueError:
                        print("Некорректный ввод зарплаты. Пожалуйста, введите число.")
                elif criterion == "3":
                    storage.delete_vacancy()
                    print("Все вакансии удалены.")
                    break
            else:
                print("Некорректный ввод. Пожалуйста, введите 1 или 2.")

        elif action == "0":
            break
        else:
            print("Неверный ввод. Попробуйте снова.")


if __name__ == "__main__":
    main()
