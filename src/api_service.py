from abc import ABC, abstractmethod
import logging
import requests
import os
from dotenv import load_dotenv


logger = logging.getLogger(__name__)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path = os.path.join(BASE_DIR, "logs", "api_service.log")
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
    """Класс для получения списка вакансий с сайта HeadHunter."""

    def __init__(self, base_url: str):
        """Инициализирует HeadHunterAPI с базовым URL"""
        logger.info("получение информации о вакансиях")
        self.base_url = base_url
        self.headers = {"User-Agent": "HH-User-Agent"}
        self.params = {"per_page": 10, "text": "", "only_with_salary": True, "salary": 0, "period": 0, "page": 0}
        self.vacancies = []

    def get_vacancies(self, required_vacancy: str, required_salary: int, required_period: int):
        """Получаем список вакансий с учетом заданных параметров"""
        logger.info(f"Запрос вакансий с параметрами: {required_vacancy}, {required_salary}, {required_period}")

        if not isinstance(required_vacancy, str) or not required_vacancy:
            error_message = f"Данная вакансия - '{required_vacancy}' - отсутствует"
            logger.error(error_message)
            raise ValueError(error_message)

        if not isinstance(required_salary, int) or required_salary <= 0:
            error_message = "Неверно указана зарплата"
            logger.error(error_message)
            raise ValueError(error_message)

        if not isinstance(required_period, int) or required_period <= 0:
            error_message = "Неверно указан период"
            logger.error(error_message)
            raise ValueError(error_message)

        self.params.update({"text": required_vacancy, "salary": required_salary, "period": required_period})

        while self.params.get("page") < 20:
            try:
                response = requests.get(url=self.base_url, headers=self.headers, params=self.params)
                response.raise_for_status()
                logger.info(f"Запрос успешно выполнен для страницы {self.params.get('page')}")

                data = response.json()
                items = data.get("items", [])

                self.vacancies.extend(items)
                self.params["page"] += 1

            except requests.RequestException as e:
                logger.error(f"Ошибка запроса к API: {e}")
                raise

        return self.vacancies


if __name__ == "__main__":
    load_dotenv()
    MY_BASE_URL = os.getenv("BASE_URL")

    hh_api = HeadHunterAPI(MY_BASE_URL)
    hh_vacancies = hh_api.get_vacancies("Python", 100000, 3)
    print(hh_vacancies)
