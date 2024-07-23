class Vacancy:
    def __init__(self, name_vacancy: str, city: str, url: str, salary: int = 0, description: str = ""):
        self.name_vacancy = name_vacancy
        self.city = city
        self.url = url
        self.salary = salary if salary is not None else 0
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
        return f"{self.name_vacancy} ({self.salary}): {self.url}\nDescription: {self.description}"


class VacancyManager:
    def __init__(self):
        self.vacancies = []

    def add_vacancy(self, vacancy: Vacancy):
        self.vacancies.append(vacancy)

    def sort_vacancies_by_salary(self):
        self.vacancies.sort(reverse=True)

    def display_vacancies(self):
        for vacancy in self.vacancies:
            print(vacancy)
            print()


if __name__ == "__main__":
    vacancy1 = Vacancy(
        "Python Developer", "Москва", "http://example.com/job1", 100000, "Develop and maintain Python applications."
    )
    vacancy2 = Vacancy(
        "Java Developer",
        "Санкт Петербург",
        "http://example.com/job2",
        120000,
        "Develop and maintain Java applications.",
    )
    vacancy3 = Vacancy(
        "Frontend Developer",
        "Воронеж",
        "http://example.com/job3",
        description="Develop and maintain frontend applications.",
    )

    manager = VacancyManager()
    manager.add_vacancy(vacancy1)
    manager.add_vacancy(vacancy2)
    manager.add_vacancy(vacancy3)
    manager.sort_vacancies_by_salary()
    manager.display_vacancies()
