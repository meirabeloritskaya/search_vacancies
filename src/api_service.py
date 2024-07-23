from abc import ABC, abstractmethod
import logging
import requests
import os
from dotenv import load_dotenv


logger = logging.getLogger(__name__)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path = os.path.join(BASE_DIR, "logs", "vacancies.log")
file_handler = logging.FileHandler(path, encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


class WebsiteAPI(ABC):
    """абстрактный класс для парсинга вакансий"""

    @abstractmethod
    def get_vacancies(self, required_vacancy: str, required_salary: int, required_period: int):
        pass


class HeadHunterAPI(WebsiteAPI):
    """получение списка вакансий"""

    def __init__(self, base_url: str):
        """получение информации о вакансиях"""
        logger.info("получение информации о вакансиях")
        self.base_url = base_url
        self.headers = {"User-Agent": "HH-User-Agent"}
        self.params = {"per_page": 10, "text": "", "only_with_salary": True, "salary": 0, "period": 0, "page": 0}
        self.vacancies = []

    def get_vacancies(self, required_vacancy: str, required_salary: int, required_period: int):

        if not isinstance(required_vacancy, str) or not required_vacancy:
            return ValueError(f"Данная вакансия  - '{required_vacancy}' - отсутствует")

        if not isinstance(required_salary, int) or required_salary <= 0:
            return ValueError("Неверно указана зарплата")

        if not isinstance(required_period, int) or required_period <= 0:
            return ValueError("Неверно указан период")

        self.params.update({"text": required_vacancy, "salary": required_salary, "period": required_period})

        while self.params.get("page") != 20:
            try:
                response = requests.get(url=self.base_url, headers=self.headers, params=self.params)
                response.raise_for_status()
            except requests.RequestException as e:
                logger.error(f"Ошибка запроса к API: {e}")
                raise

            data = response.json()
            items = data.get("items", [])
            self.vacancies.extend(items)  # Добавляем вакансии в список
            self.params["page"] += 1  # Переходим к следующей странице

        return self.vacancies


if __name__ == "__main__":
    load_dotenv()
    MY_BASE_URL = os.getenv("BASE_URL")

    hh_api = HeadHunterAPI(MY_BASE_URL)
    hh_vacancies = hh_api.get_vacancies("Python", 100000, 3)
    print(hh_vacancies)
