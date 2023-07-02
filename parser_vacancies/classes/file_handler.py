import os
from abc import ABC, abstractmethod

from parser_vacancies.classes.vacancies_handler import VacanciesHandler
from parser_vacancies.constants import DATA_DIR


class FileHandler(ABC):
    """Абстрактный родительский класс для работы с файлами"""
    @abstractmethod
    def __init__(self, file_name: str):
        """Инициализация экземпляра через имя файла"""
        # проверка существования каталога для файлов, добавление при необходимости
        if not os.path.isdir(DATA_DIR):
            os.mkdir(DATA_DIR)
        pass

    @abstractmethod
    def overwrite_vacancies(self, vacancies: VacanciesHandler) -> None:
        """Перезаписывает вакансии в файл (старое содержимое удаляет, новое записывает)"""
        pass

    @abstractmethod
    def add_vacancies(self, vacancies: VacanciesHandler) -> None:
        """Дозаписывает вакансии в файл (старое содержимое НЕ удаляет, новое записывает в конец)"""
        pass

    @abstractmethod
    def read_vacancies(self) -> VacanciesHandler:
        """Считывает вакансии из файла"""
        pass

    @staticmethod
    @abstractmethod
    def convert_vacancies_to_data(vacancies: VacanciesHandler) -> list:
        """Переводит данные из формата, полученного из файла, в формат VacanciesHandler"""
        pass

    @staticmethod
    @abstractmethod
    def convert_data_to_vacancies(data) -> VacanciesHandler:
        """Переводит данные из формата VacanciesHandler в формат для записи в файл"""
        pass

    @abstractmethod
    def is_file_exist(self) -> bool:
        """Проверяет, есть ли файл с таким именем"""
        pass

    @abstractmethod
    def delete_file(self) -> None:
        """Удаляет файл"""
        pass






