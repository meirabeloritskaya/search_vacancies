from abc import ABC, abstractmethod
import json
import os


class VacancyStorage(ABC):
    @abstractmethod
    def add_vacancy(self, vacancy):
        pass

    @abstractmethod
    def get_vacancies(self, **criteria):
        pass

    @abstractmethod
    def delete_vacancy(self, **criteria):
        pass

    @abstractmethod
    def sorted_vacancies(self, reverse=False):
        pass

    @abstractmethod
    def top_n_vacancies(self, n):
        pass


class JsonVacancyStorage(VacancyStorage):
    def __init__(self, file_path):
        self.file_path = file_path

        if not os.path.exists(self.file_path):
            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump([], file)

    def _load_vacancies(self):
        with open(self.file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def _save_vacancies(self, vacancies):
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(vacancies, file)

    def add_vacancy(self, vacancy):
        vacancies = self._load_vacancies()
        vacancies.append(vacancy.__dict__)
        self._save_vacancies(vacancies)

    def get_vacancies(self, **criteria):
        vacancies = self._load_vacancies()
        return [vacancy for vacancy in vacancies if all(vacancy.get(key) == value for key, value in criteria.items())]

    def sorted_vacancies(self, reverse=False):
        vacancies = self._load_vacancies()
        sorted_vacancies = sorted(vacancies, key=lambda x: x.get("salary", 0), reverse=reverse)
        return sorted_vacancies

    def top_n_vacancies(self, n):
        sorted_vacancies = self.sorted_vacancies(revers=True)
        return sorted_vacancies[:n]

    def delete_vacancy(self, **criteria):
        vacancies = self._load_vacancies()
        rest_vacancies = [
            vacancy for vacancy in vacancies if not all(vacancy.get(key) == value for key, value in criteria.items())
        ]
        self._save_vacancies(rest_vacancies)
