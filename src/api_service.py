from abc import ABC, abstractmethod
import logging
from src.processing_vacancies import Vacancy
import requests
from accessify import private
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
    def get_vacancies(self, required_vacancy, required_salary, required_period):
        pass


class HeadHunterAPI(WebsiteAPI):
    """получение списка вакансий"""

    def __init__(self, BASE_URL):
        """получение информации о вакансиях"""
        logger.info("получение информации о вакансиях")
        self.base_url = BASE_URL
        # self.vacancies = []

    def get_vacancies(self, required_vacancy, required_salary, required_period):

        params = {
            "per_page": 50,
            "text": required_vacancy,
            "only_with_salary": True,
            "salary": required_salary,
            "period": required_period,
        }
        response = requests.get(url=self.base_url, params=params)
        if response.status_code != 200:
            raise Exception(f"Ошибка запроса к API: Статус {response.status_code}")

        vacancies_list = response.json()["items"]
        return vacancies_list

        # self.vacancies = Vacancy.cast_to_object_list(vacancies_list)


if __name__ == "__main__":
    load_dotenv()
    MY_BASE_URL = os.getenv("BASE_URL")
    hh_api = HeadHunterAPI(MY_BASE_URL)
    hh_vacancies = hh_api.get_vacancies("Python", 100000, 3)
    print(hh_vacancies)
