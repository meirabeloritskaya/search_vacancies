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

    def vacancies_by_keyword(self, keyword: str):
        """Фильтрует вакансии по ключевому слову в описании."""
        vacancies = [vacancy for vacancy in self.vacancies if keyword.lower() in vacancy.description.lower()]
        return vacancies

    def display_filtered_vacancies(self, keyword: str):
        """Отображает вакансии, содержащие ключевое слово в описании."""
        filtered_vacancies = self.vacancies_by_keyword(keyword)
        if not filtered_vacancies:
            print(f"Нет вакансий, содержащих ключевое слово '{keyword}' в описании.")
        else:
            for vacancy in filtered_vacancies:
                print(vacancy)
                print()

    def top_vacancies(self, n):
        # while True:                                                           #НЕ РАБОТАЕТ!!!
        #    try:
        #         n = int(top_n)
        #         if n <= 0:
        #             print("Пожалуйста, введите целое положительное целое число.")
        #             raise ValueError
        #             break
        #    except ValueError:
        #        print("Пожалуйста, введите целое положительное целое число.")

        top_vacancies = self.vacancies[:n]
        return top_vacancies


if __name__ == "__main__":

    load_dotenv()
    base_url = os.getenv("BASE_URL")

    manager = VacancyManager(base_url)
    query = input("Введите название вакансии: ")
    keyword = input("Введите ключевое слово для фильтрации вакансий по описанию: ").strip()
    salary = int(input("Введите желаемую зарплату: "))
    period = int(input("Введите период (в днях): "))
    top_n = int(input("Введите количество топ вакансий для отображения: "))

    print("_____________")
    print()
    manager.fetch_vacancies(query, salary, period)
    manager.display_filtered_vacancies(keyword)
    manager.sort_vacancies_by_salary()
    top_n_vacancies = manager.top_vacancies(top_n)
    for vacancy in top_n_vacancies:
        print(vacancy)
        print()
