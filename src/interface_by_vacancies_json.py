from abc import ABC, abstractmethod
import json
import os
import logging


logger = logging.getLogger(__name__)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path = os.path.join(BASE_DIR, "logs", "interface_by_vacancies_json.log")
file_handler = logging.FileHandler(path, encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


class VacancyStorage(ABC):
    @abstractmethod
    def add_vacancy(self, vacancy):
        """Добавляет новую вакансию в хранилище."""
        pass

    @abstractmethod
    def get_vacancies(self, **criteria):
        """Возвращает список вакансий, удовлетворяющих заданным критериям."""
        pass

    @abstractmethod
    def delete_vacancy(self, **criteria):
        """Удаляет вакансии, соответствующие заданным критериям."""
        pass

    @abstractmethod
    def sorted_vacancies(self, order):
        """Возвращает отсортированный список вакансий по зарплате."""
        pass

    @abstractmethod
    def top_n_vacancies(self, n):
        """Возвращает топ N вакансий с наивысшей зарплатой."""
        pass


class JsonVacancyStorage(VacancyStorage):
    def __init__(self, file_path):
        """Инициализация хранилища вакансий в JSON файле"""
        self.file_path = file_path

        if not os.path.exists(self.file_path):
            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump([], file)
                logger.info(f"Создан новый файл вакансий: {self.file_path}")

    def _load_vacancies(self):
        """Загружает вакансии из JSON файла"""
        with open(self.file_path, "r", encoding="utf-8") as file:
            logger.info(f"Загрузка вакансий из файла: {self.file_path}")
            return json.load(file)

    def _save_vacancies(self, vacancies):
        """Сохраняет вакансии в JSON файл"""
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(vacancies, file)
            logger.info(f"Вакансии сохранены в файл: {self.file_path}")

    def add_vacancy(self, vacancy):
        """Добавляет новую вакансию в хранилище"""
        vacancies = self._load_vacancies()
        vacancies.append(vacancy.__dict__)
        self._save_vacancies(vacancies)
        logger.info(f"Добавлена новая вакансия: {vacancy}")

    def get_vacancies(self, **criteria):
        """Возвращает список вакансий, удовлетворяющих заданным критериям"""
        vacancies = self._load_vacancies()
        filtered_vacancies = [
            vacancy for vacancy in vacancies if all(vacancy.get(key) == value for key, value in criteria.items())
        ]
        logger.info(f"Найдено {len(filtered_vacancies)} вакансий по критериям: {criteria}")
        return filtered_vacancies

    def sorted_vacancies(self, reverse):
        """Возвращает отсортированный список вакансий по зарплате"""
        vacancies = self._load_vacancies()
        sorted_vacancies = sorted(vacancies, key=lambda x: x.get("salary", 0), reverse=reverse)
        logger.info(f"Вакансии отсортированы по зарплате. Обратный порядок: {reverse}")
        return sorted_vacancies

    def top_n_vacancies(self, n):
        """Возвращает топ N вакансий с наивысшей зарплатой"""
        sorted_vacancies = self.sorted_vacancies(reverse=True)
        top_vacancies = sorted_vacancies[:n]
        logger.info(f"Топ {n} вакансий с наивысшей зарплатой: {top_vacancies}")
        return top_vacancies

    def delete_vacancy(self, **criteria):
        """Удаляет вакансии, соответствующие заданным критериям"""
        vacancies = self._load_vacancies()
        rest_vacancies = [
            vacancy for vacancy in vacancies if not all(vacancy.get(key) == value for key, value in criteria.items())
        ]
        self._save_vacancies(rest_vacancies)
        logger.info(f"Удалены вакансии по критериям: {criteria}. Осталось вакансий: {len(rest_vacancies)}")
        return rest_vacancies
