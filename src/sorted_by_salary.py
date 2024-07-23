from src.api_service import HeadHunterAPI
import os
from dotenv import load_dotenv


class Vacancy:
    def __init__(
        self, name_vacancy: str, city: str, url: str, salary: int = 0, currency: str = "", description: str = ""
    ):
        self.name_vacancy = name_vacancy
        self.city = city
        self.url = url
        self.salary = salary if salary is not None else 0
        self.currency = currency
        self.description = description
        self._validate()

    def _validate(self):
        """валидация данных"""
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

        return cls(
            name_vacancy=vacancy_data.get("name", ""),
            city=vacancy_data.get("area", {}).get("name", "Не указан"),
            url=vacancy_data.get("alternate_url", ""),
            salary=vacancy_data.get("salary", {}).get("from", 0),
            currency=vacancy_data.get("salary", {}).get("currency", "Не указано"),
            description=vacancy_data.get("snippet", {}).get("requirement", "Не указано"),
        )

    def __lt__(self, other):
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary < other.salary

    def __le__(self, other):
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary <= other.salary

    def __eq__(self, other):
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary == other.salary

    def __ne__(self, other):
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary != other.salary

    def __gt__(self, other):
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary > other.salary

    def __ge__(self, other):
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary >= other.salary

    def __str__(self):
        return f"{self.name_vacancy} ({self.salary}, {self.currency}): {self.url}\nDescription: {self.description}"


class VacancyManager:
    def __init__(self, base_url: str):
        self.api = HeadHunterAPI(base_url)
        self.vacancies = []

    def fetch_vacancies(self, query: str, salary: int, period: int):
        vacancies_data = self.api.get_vacancies(query, salary, period)
        self.vacancies = [
            Vacancy.from_api(vacancy)
            for vacancy in vacancies_data
            if vacancy.get("salary", {}).get("from") is not None and vacancy.get("salary", {}).get("from") >= salary
        ]

    def add_vacancy(self, vacancy: Vacancy):
        self.vacancies.append(vacancy)

    def sort_vacancies_by_salary(self):
        self.vacancies.sort(reverse=True)

    def display_vacancies(self):
        for vacancy in self.vacancies:
            print(vacancy)
            print()


def main():
    load_dotenv()
    base_url = os.getenv("BASE_URL")

    manager = VacancyManager(base_url)
    query = input("Введите название вакансии: ")
    salary = int(input("Введите желаемую зарплату: "))
    period = int(input("Введите период (в днях): "))

    manager.fetch_vacancies(query, salary, period)
    manager.sort_vacancies_by_salary()
    manager.display_vacancies()


if __name__ == "__main__":
    main()
