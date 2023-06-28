import os
from abc import ABC, abstractmethod

from parser_vacancies.classes.vacancies_handler import VacanciesHandler
from parser_vacancies.constants import DATA_DIR


class FileHandler(ABC):
    @abstractmethod
    def __init__(self, file_name: str):
        """инициализация экземпляра через имя файла"""
        # проверка на существование каталога для файлов
        if not os.path.isdir(DATA_DIR):
            os.mkdir(DATA_DIR)
        pass

    @abstractmethod
    def overwrite_vacancies(self, vacancies: VacanciesHandler) -> None:
        """перезаписывает данные в файл (старое содержимое удаляет, новое записывает)"""
        pass

    @abstractmethod
    def add_vacancies(self, vacancies: VacanciesHandler) -> None:
        """дозаписывает данные в файл (старое содержимое НЕ удаляет, новое записывает в конец)"""
        pass

    @abstractmethod
    def read_vacancies(self) -> VacanciesHandler:
        """считывает вакансии из файла"""
        pass

    @staticmethod
    @abstractmethod
    def convert_vacancies_to_data(vacancies: VacanciesHandler) -> list:
        """переводит данные из формата VacanciesHandler в формат для записи в файл"""
        pass

    @staticmethod
    @abstractmethod
    def convert_data_to_vacancies(data) -> VacanciesHandler:
        """переводит данные из формата, полученного из файла, в формат VacanciesHandler"""
        pass

    @abstractmethod
    def is_file_exist(self) -> bool:
        """проверяет, есть ли файл с таким именем"""
        pass

    @abstractmethod
    def delete_file(self) -> None:
        """удаляет файл"""
        pass






class ExcelFileHandler(FileHandler):
    pass
