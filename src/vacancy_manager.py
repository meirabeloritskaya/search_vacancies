from src.api_service import HeadHunterAPI
import os
from dotenv import load_dotenv
import logging


logger = logging.getLogger(__name__)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path = os.path.join(BASE_DIR, "logs", "vacancy_manager.log")
file_handler = logging.FileHandler(path, encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


class Vacancy:
    """Класс для представления вакансии"""
    def __init__(
        self, name_vacancy: str, city: str, url: str, salary: int = 0, currency: str = "", description: str = ""
    ):
        """Инициализация вакансии и проверка данных"""
        self.name_vacancy = name_vacancy
        self.city = city
        self.url = url
        self.salary = salary if salary is not None else 0
        self.currency = currency
        self.description = description
        self._validate()

    def _validate(self):
        """Валидация данных вакансии"""
        if not self.name_vacancy:
            raise ValueError("Название вакансии не может быть пустым")
        if not self.url or not self.url.startswith("http"):
            raise ValueError("Неверная ссылка на вакансию")
        if not isinstance(self.salary, int) or self.salary < 0:
            raise ValueError("Неверно указана зарплата")
        if not isinstance(self.description, str):
            raise ValueError("Описание должно быть строкой")

    @classmethod
    def from_api(cls, vacancy_data):
        """Создает экземпляр Vacancy из данных API"""

        description = vacancy_data.get("snippet", {}).get("requirement", "Не указано")
        if not isinstance(description, str):
            description = "Не указано"

        return cls(
            name_vacancy=vacancy_data.get("name", ""),
            city=vacancy_data.get("area", {}).get("name", "Не указан"),
            url=vacancy_data.get("alternate_url", ""),
            salary=vacancy_data.get("salary", {}).get("from", 0),
            currency=vacancy_data.get("salary", {}).get("currency", "Не указано"),
            description=description,
        )

    def __lt__(self, other):
        """Сравнение вакансий по зарплате (меньше чем)"""
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary < other.salary

    def __le__(self, other):
        """Сравнение вакансий по зарплате (меньше или равно)"""
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary <= other.salary

    def __eq__(self, other):
        """Сравнение вакансий по зарплате (равно)"""
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary == other.salary

    def __ne__(self, other):
        """Сравнение вакансий по зарплате (не равно)"""
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary != other.salary

    def __gt__(self, other):
        """Сравнение вакансий по зарплате (больше чем)"""
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary > other.salary

    def __ge__(self, other):
        """Сравнение вакансий по зарплате (больше или равно)"""
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary >= other.salary

    def __str__(self):
        """Возвращает строковое представление вакансии"""
        return f"{self.name_vacancy} ({self.salary}, {self.currency}): {self.url}\nDescription: {self.description}"


class VacancyManager:
    """Класс для управления вакансиями"""
    def __init__(self, base_url: str):
        """Инициализация менеджера вакансий"""
        logger.info("Инициализация VacancyManager с базовым URL")
        self.api = HeadHunterAPI(base_url)
        self.vacancies = []

    def fetch_vacancies(self, query: str, salary: int, period: int):
        """Получаем вакансии по запросу и фильтрует их по минимальной зарплате"""
        logger.info(f"Получение вакансий по запросу: {query}, зарплата: {salary}, период: {period}")
        vacancies_data = self.api.get_vacancies(query, salary, period)
        self.vacancies = [
            Vacancy.from_api(vacancy)
            for vacancy in vacancies_data
            if vacancy.get("salary", {}).get("from") is not None and vacancy.get("salary", {}).get("from") >= salary
        ]
        logger.info(f"Получено {len(self.vacancies)} вакансий.")

    def add_vacancy(self, vacancy: Vacancy):
        """Добавляет вакансию в список"""
        logger.info(f"Добавление вакансии: {vacancy}")
        self.vacancies.append(vacancy)

    def vacancies_by_keyword(self, keyword: str):
        """Фильтрует вакансии по ключевому слову в описании."""
        logger.info(f"Фильтрация вакансий по ключевому слову: {keyword}"
        vacancies = [vacancy for vacancy in self.vacancies if keyword.lower() in vacancy.description.lower()]
        return vacancies

    def display_filtered_vacancies(self, keyword: str):
        """Отображает вакансии, содержащие ключевое слово в описании."""
        filtered_vacancies = self.vacancies_by_keyword(keyword)
        if not filtered_vacancies:
            print(f"Нет вакансий, содержащих ключевое слово '{keyword}' в описании.")
            logger.info(f"Нет вакансий, содержащих ключевое слово '{keyword}' в описании.")
        return filtered_vacancies


if __name__ == "__main__":

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
    vacancies = manager.display_filtered_vacancies(keyword)

    for vacancy in vacancies:
        print(vacancy)
        print()
