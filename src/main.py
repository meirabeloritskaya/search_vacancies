import os
import logging
from interface_by_vacancies_json import VacancyApp

logger = logging.getLogger(__name__)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path = os.path.join(BASE_DIR, "logs", "main.log")
file_handler = logging.FileHandler(path, encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


def run_app(app):
    """Запуск основного цикла приложения."""
    while True:
        action = input(
            "Выберите действие: \n"
            "(0) Выход\n"
            "(1) Добавить вакансию в JSON файл\n"
            "(2) Получить вакансии из JSON файла\n"
            "(3) Вывести сортированный список вакансий\n"
            "(4) Вывести топ-n вакансий\n"
            "(5) Удалить вакансию из JSON файла\n"
        ).strip()

        if action == "1":
            app.add_vacancies()
        elif action == "2":
            app.get_vacancies()
        elif action == "3":
            app.sort_vacancies()
        elif action == "4":
            app.top_n_vacancies()
        elif action == "5":
            app.delete_vacancies()
        elif action == "0":
            logger.info("Программа завершена пользователем.")
            break
        else:
            print("Неверный ввод. Попробуйте снова.")
            logger.warning("Неверный ввод действия: %s", action)


if __name__ == "__main__":
    storage_path = os.path.join(BASE_DIR, "data", "vacancies.json")
    app = VacancyApp(storage_path)
    run_app(app)
