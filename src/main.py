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
                "Выберите действие: "
                "(1) Добавить вакансию "
                "(2) Получить вакансии "
                "(3) Сортировать вакансии"
                "(4) Удалить вакансию "
                "(0) Выход: ")
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
                    criteria['city'] = city
                if salary_min is not None:
                    criteria['salary'] = salary_min

                filtered_vacancies = storage.get_vacancies(**criteria)
                print("Фильтрованные вакансии:")
                for vacancy in filtered_vacancies:
                    print(vacancy)

            elif action == "3":
                 # Сортировка вакансий
                 sort_by = input("Введите поле для сортировки (например, 'salary'): ")
                 order = input("Введите порядок сортировки (asc/desc): ")
                 ascending = order.lower() == "asc"

                 with open(path, 'r', encoding="utf-8") as file:
                     vacancies = json.load(file)

                 sorted_vacancies = sorted(vacancies, key=lambda x: x.get(sort_by, 0), reverse=not ascending)
                 print("Отсортированные вакансии:")
                 for vacancy in sorted_vacancies:
                     print(vacancy)

            elif action == "4":
                # Удаление вакансии
                criteria = {}
                criterion = input("Удалить по (1) городу (2) зарплате: ")
                if criterion == "1":
                    city = input("Введите город для удаления: ")
                    criteria['city'] = city
                elif criterion == "2":
                    salary = input("Введите зарплату для удаления: ")
                    criteria['salary'] = int(salary)
                storage.delete_vacancy(**criteria)

            elif action == "0":
                break
            else:
                print("Неверный ввод. Попробуйте снова.")


if __name__ == "__main__":
    main()
