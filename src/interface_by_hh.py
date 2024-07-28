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


class HHInterface:
    def __init__(self):
        """Инициализация класса HHInterface, настройка логирования и загрузка переменных окружения."""
        load_dotenv()
        self.base_url = os.getenv("BASE_URL")
        self.manager = VacancyManager(self.base_url)
        logger.info("HHInterface инициализирован.")
    def interface_hh(self):
        """Запрос параметров поиска вакансий у пользователя и их возврат."""
        logger.info("Получение ввода пользователя для параметров поиска вакансий.")

        while True:
            query = input("Введите название вакансии: ").strip()
            if not query:
                print("Ошибка: Название вакансии не может быть пустым. Пожалуйста, введите корректное значение.")
                logger.warning("Пользователь ввел пустое название вакансии.")
            else:
                break

        keyword = input("Введите ключевое слово для фильтрации вакансий по описанию (или оставьте пустым): ").strip()

        while True:
            salary_input = input("Введите числом желаемую зарплату: ")
            if not salary_input.isdigit():
                print("Ошибка: Зарплата должна быть числом. Пожалуйста, введите корректное значение.")
                logger.warning(f"Пользователь ввел некорректную зарплату: {salary_input}.")
            else:
                salary = int(salary_input)
                break

        while True:
            period_input = input("Введите период (в днях): ")
            if not period_input.isdigit():
                print("Ошибка: Период должен быть числом. Пожалуйста, введите корректное значение.")
                logger.warning(f"Пользователь ввел некорректный период: {period_input}.")
            else:
                period = int(period_input)
                break
        logger.info("Ввод пользователя успешно получен.")
        return query, keyword, salary, period

    def get_data(self):
        """Запуск интерфейса для получения и отображения вакансий на основе ввода пользователя."""
        logger.info("Запуск метода run класса HHInterface.")
        query, keyword, salary, period = self.interface_hh()

        print("_____________")
        print()
        self.manager.fetch_vacancies(query, salary, period)
        vacancies_hh = self.manager.display_filtered_vacancies(keyword)

        return vacancies_hh


if __name__ == "__main__":
    interface = HHInterface()
    vacancies = interface.get_data()
    if vacancies:
        for vacancy in vacancies:
            print(vacancy)
            print()
            logger.info("Вакансии успешно отображены.")
    else:
        print("Нет вакансий для отображения.")
        logger.info("Нет вакансий для отображения.")