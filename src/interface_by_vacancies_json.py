from abc import ABC, abstractmethod
import json
import os
from dotenv import load_dotenv


class VacancyStorage(ABC):
    @abstractmethod
    def add_vacancy(self, vacancy):
        pass

    @abstractmethod
    def get_vacancies(self, **criteria):
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy_id):
        pass


class JsonVacancyStorage(VacancyStorage):
    def __init__(self, file_path):
        self.file_path = file_path
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump([], file)

    def add_vacancy(self, vacancy):
        with open(self.file_path, "r", encoding="utf-8") as file:
            vacancies = json.load(file)
        vacancies.append(vacancy.__dict__)
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(vacancies, file)

    def get_vacancies(self, **criteria):
        with open(self.file_path, "r", encoding="utf-8") as file:
            vacancies = json.load(file)
        return [vacancy for vacancy in vacancies if all(vacancy.get(k) == v for k, v in criteria.items())]

    def delete_vacancy(self, **criteria):
        with open(self.file_path, "r", encoding="utf-8") as file:
            vacancies = json.load(file)
        vacancies = [vacancy for vacancy in vacancies if not all(vacancy.get(k) == v for k, v in criteria.items())]
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(vacancies, file, ensure_ascii=False, indent=4)
