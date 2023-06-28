import json
import os.path

from parser_vacancies.classes.file_handler import FileHandler
from parser_vacancies.classes.vacancies_handler import VacanciesHandler
from parser_vacancies.classes.vacancy import Vacancy
from parser_vacancies.constants import DATA_DIR


class JSONFileHandler(FileHandler):
    def __init__(self, file_name: str):
        """инициализация экземпляра через имя файла.
        добавляется путь к папке с файлами и расширение файла"""
        super().__init__(file_name)
        self.file_name = os.path.join(DATA_DIR, f'{file_name}.json')

    def overwrite_vacancies(self, vacancies: VacanciesHandler) -> None:
        """перезаписывает данные в файл (старое содержимое удаляет, новое записывает)"""
        prepared_data = self.convert_vacancies_to_data(vacancies)
        with open(self.file_name, 'w', encoding='utf-8') as file:
            json.dump(prepared_data, file, indent=2, ensure_ascii=False)

    def add_vacancies(self, vacancies: VacanciesHandler) -> None:
        """дозаписывает данные в файл (старое содержимое НЕ удаляет, новое записывает в конец)"""
        full_vacancies = self.read_vacancies()
        full_vacancies.extend(vacancies)
        prepared_data = self.convert_vacancies_to_data(full_vacancies)
        with open(self.file_name, 'w', encoding='utf-8') as file:
            json.dump(prepared_data, file, indent=2, ensure_ascii=False)

    def read_vacancies(self) -> VacanciesHandler:
        """считывает вакансии из файла"""
        data_from_file = ''
        with open(self.file_name, 'r', encoding='utf-8') as file:
            try:
                data_from_file = json.load(file)
            except json.decoder.JSONDecodeError:
                print('Данные в файле не соответствуют формату JSON')
        return self.convert_data_to_vacancies(data_from_file)

    @staticmethod
    def convert_data_to_vacancies(data) -> VacanciesHandler:
        """переводит данные из формата, полученного из файла, в формат VacanciesHandler"""
        vacancies = VacanciesHandler()
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
        """переводит данные из формата VacanciesHandler в формат для записи в файл"""
        prepared_data = []
        for vacancy in vacancies:
            prepared_data.append(vacancy.__dict__)
        return prepared_data

    def is_file_exist(self) -> bool:
        """проверяет, есть ли файл с таким именем"""
        return os.path.isfile(self.file_name)

    def delete_file(self) -> None:
        """удаляет файл"""
        if self.is_file_exist():
            os.remove(self.file_name)


# РАБОЧЕЕ ДЛЯ ПРОВЕРКИ
vacancy1 = Vacancy('hhvacancy_id1', 'title1', 'url1', 'description1',
                   20, 40, False,
                   '2023-06-25', 'town1')

vacancy2 = Vacancy('sjvacancy_id2', 'title2', 'url2', 'description2',
                   None, 50, False,
                   '2023-06-27', 'town2')

vacancy3 = Vacancy('sjvacancy_id3', 'tile3', 'url3', 'description3',
                   None, None, True,
                   '2023-06-26', 'town3')

vacancies = VacanciesHandler([vacancy1, vacancy2, vacancy3])
json_fh = JSONFileHandler('test1')
json_fh.overwrite_vacancies(vacancies)
vacancies2 = VacanciesHandler(json_fh.read_vacancies())
print(vacancies2)
