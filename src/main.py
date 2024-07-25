import os
from dotenv import load_dotenv
from src.interface_by_hh import interface_hh
from src.interface_by_vacancies_json import JsonVacancyStorage
import json


def main():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(BASE_DIR, "data", "vacancies.json")
    load_dotenv()

    storage = JsonVacancyStorage(path)

    while True:
        action = input(
            "Выберите действие:\n "
            "(1) Добавить вакансию \n"
            "(2) Получить вакансии \n"
            "(3) Сортировать вакансии\n"
            "(4) Удалить вакансию\n "
            "(0) Выход: \n"
        )
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
            order = input("Введите порядок сортировки (asc/desc): ").strip().lower()
            if order not in ["asc", "desc"]:
                print(
                    "Ошибка: Пожалуйста, введите 'asc' для сортировки по возрастанию или 'desc' для сортировки по убыванию."
                )
                continue

            ascending = order == "asc"

            with open(path, "r", encoding="utf-8") as file:
                try:
                    vacancies = json.load(file)
                except json.JSONDecodeError:
                    vacancies = []

            sorted_vacancies = sorted(vacancies, key=lambda x: x.get("salary", 0), reverse=not ascending)
            print("Отсортированные вакансии:")
            for vacancy in sorted_vacancies:
                print(vacancy)

        elif action == "4":
            # Удаление вакансии
            criteria = {}
            criterion = input("Удалить по (1) городу (2) зарплате: ").strip()
            if criterion == "1":
                city = input("Введите город для удаления: ").strip().capitalize()
                criteria["city"] = city
            elif criterion == "2":
                salary = input("Введите зарплату для удаления: ").strip()
                criteria["salary"] = int(salary)
            storage.delete_vacancy(**criteria)

        elif action == "0":
            break
        else:
            print("Неверный ввод. Попробуйте снова.")


if __name__ == "__main__":
    main()
