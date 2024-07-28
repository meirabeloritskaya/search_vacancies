import os
import logging
from dotenv import load_dotenv
from src.interface_by_hh import HHInterface
from src.service_by_vacancies_json import JsonVacancyStorage

# Настройка логирования
logger = logging.getLogger(__name__)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log_path = os.path.join(BASE_DIR, "logs", "main.log")
file_handler = logging.FileHandler(log_path, encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


class VacancyApp:
    """Класс для управления приложением вакансий."""

    def __init__(self, storage_path):
        """Инициализация приложения"""
        self.storage = JsonVacancyStorage(storage_path)
        load_dotenv()
        logger.info("VacancyApp инициализирован с путем: %s", storage_path)

    def add_vacancies(self):
        """Добавляет вакансии в JSON файл."""
        interface = HHInterface()
        vacancies = interface.get_data()
        for vacancy in vacancies:
            self.storage.add_vacancy(vacancy)
        print("Вакансии добавлены в файл.")
        logger.info("Вакансии добавлены в файл.")

    def get_vacancies(self):
        """Получает и фильтрует вакансии из JSON файла."""
        city = input("Введите город для фильтрации (или оставьте пустым): ").strip()
        salary_min = input("Введите минимальную зарплату (или оставьте пустым): ").strip()
        salary_min = int(salary_min) if salary_min else None

        criteria = {}
        if city:
            criteria["city"] = city
        if salary_min is not None:
            criteria["salary"] = salary_min

        filtered_vacancies = self.storage.get_vacancies(**criteria)
        filtered_vacancies = [
            vacancy for vacancy in filtered_vacancies if not city or vacancy["city"].lower() == city.lower()
        ]

        if not filtered_vacancies:
            print("Не найдено вакансий по указанным критериям.")
            logger.info("Не найдено вакансий по указанным критериям.")
        else:
            print("Фильтрованные вакансии:")
            for vacancy in filtered_vacancies:
                print(vacancy)
            logger.info("Отображены фильтрованные вакансии.")

    def sort_vacancies(self):
        """Вывести отсортированный список вакансий."""
        while True:
            order = input("Введите порядок сортировки (asc/desc): ").strip().lower()
            if order not in ["asc", "desc"]:
                print(
                    "Ошибка: Пожалуйста, введите 'asc' для сортировки по возрастанию или 'desc' для сортировки по убыванию."
                )
                logger.warning("Некорректный ввод порядка сортировки.")
                continue

            sorted_vacancies = self.storage.sorted_vacancies(order == "desc")
            print("Отсортированные вакансии:")
            for vacancy in sorted_vacancies:
                print(vacancy)
            logger.info("Отображены отсортированные вакансии.")
            break

    def top_n_vacancies(self):
        """Выводим топ-n вакансий."""
        n = input("Введите количество топ вакансий: ").strip()
        try:
            n = int(n)
            if n <= 0:
                print("Введите положительное целое число.")
                logger.warning("Введено некорректное количество топ вакансий: %s", n)
            else:
                top_vacancies = self.storage.sorted_vacancies(True)[:n]
                for vacancy in top_vacancies:
                    print(vacancy)
                logger.info("Отображены топ-%d вакансии.", n)
        except ValueError:
            print("Введите положительное целое число.")
            logger.warning("Некорректный ввод количества топ вакансий: %s", n)

    def delete_vacancies(self):
        """Удаляем вакансии из JSON файла."""
        while True:
            criterion = input(
                "Удалить по городу (введите цифру 1)\n"
                "Удалить по зарплате (введите цифру 2)\n"
                "Удалить все вакансии (введите цифру 3): "
            ).strip()

            if criterion == "1":
                city = input("Введите город для удаления: ").strip().capitalize()
                self.storage.delete_vacancy(city=city)
                print(f"Вакансии из города {city} удалены.")
                logger.info("Вакансии из города %s удалены.", city)
                break

            elif criterion == "2":
                salary = input("Введите зарплату для удаления: ").strip()
                try:
                    salary = int(salary)
                    self.storage.delete_vacancy(salary=salary)
                    print(f"Вакансии с зарплатой {salary} удалены.")
                    logger.info("Вакансии с зарплатой %d удалены.", salary)
                    break
                except ValueError:
                    print("Некорректный ввод зарплаты. Пожалуйста, введите число.")
                    logger.warning("Некорректный ввод зарплаты для удаления: %s", salary)

            elif criterion == "3":
                self.storage.delete_vacancy()
                print("Все вакансии удалены.")
                logger.info("Все вакансии удалены.")
                break

            else:
                print("Некорректный ввод. Пожалуйста, введите 1, 2 или 3.")
                logger.warning("Некорректный ввод при удалении вакансий: %s", criterion)
