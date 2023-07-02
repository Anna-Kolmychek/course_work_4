import json
import os.path

from parser_vacancies.classes.file_handler import FileHandler
from parser_vacancies.classes.vacancies_handler import VacanciesHandler
from parser_vacancies.classes.vacancy import Vacancy
from parser_vacancies.constants import DATA_DIR


class JSONFileHandler(FileHandler):
    """Класс для работы с файлом .json"""
    def __init__(self, file_name: str):
        """Инициализация экземпляра через имя файла.
        К имени добавляется путь к папке с файлами и расширение файла."""
        super().__init__(file_name)
        self.file_name = os.path.join(DATA_DIR, f'{file_name}.json')

    def overwrite_vacancies(self, vacancies: VacanciesHandler) -> None:
        """Перезаписывает вакансии в файл (старое содержимое удаляет, новое записывает)"""
        prepared_data = self.convert_vacancies_to_data(vacancies)
        with open(self.file_name, 'w', encoding='utf-8') as file:
            json.dump(prepared_data, file, indent=2, ensure_ascii=False)

    def add_vacancies(self, vacancies: VacanciesHandler) -> None:
        """Дозаписывает вакансии в файл (старое содержимое НЕ удаляет, новое записывает в конец)"""
        full_vacancies = self.read_vacancies()
        full_vacancies.extend(vacancies)
        prepared_data = self.convert_vacancies_to_data(full_vacancies)
        with open(self.file_name, 'w', encoding='utf-8') as file:
            json.dump(prepared_data, file, indent=2, ensure_ascii=False)

    def read_vacancies(self) -> VacanciesHandler:
        """Считывает вакансии из файла"""
        data_from_file = ''
        with open(self.file_name, 'r', encoding='utf-8') as file:
            try:
                data_from_file = json.load(file)
            except json.decoder.JSONDecodeError:
                print('Данные в файле не соответствуют формату JSON')
        return self.convert_data_to_vacancies(data_from_file)

    @staticmethod
    def convert_data_to_vacancies(data) -> VacanciesHandler:
        """Переводит данные из формата, полученного из файла, в формат VacanciesHandler"""
        vacancies = VacanciesHandler([])
        for item in data:
            vacancy = Vacancy(item['vacancy_id'],
                              item['title'],
                              item['url'],
                              item['description'],
                              item['payment_from'],
                              item['payment_to'],
                              item['distant_work'],
                              item['date_published'],
                              item['town'])
            vacancies.append(vacancy)
        return vacancies

    @staticmethod
    def convert_vacancies_to_data(vacancies: VacanciesHandler) -> list:
        """Переводит данные из формата VacanciesHandler в формат для записи в файл"""
        prepared_data = []
        for vacancy in vacancies:
            prepared_data.append(vacancy.__dict__)
        return prepared_data

    def is_file_exist(self) -> bool:
        """Проверяет, есть ли файл с таким именем"""
        return os.path.isfile(self.file_name)

    def delete_file(self) -> None:
        """Удаляет файл"""
        if self.is_file_exist():
            os.remove(self.file_name)
