from abc import ABC, abstractmethod


class JobSitesAPI(ABC):
    """Абстрактный родительский класс для работы с API разных сайтов с вакансиями"""
    @abstractmethod
    def __init__(self):
        """Инициализация API, задаем headers и базовый url для работы с API"""
        pass

    @abstractmethod
    def get_vacancies(self, user_search_params: dict):
        """Получает по API вакансии с заданными параметрами,
           возвращает список вакансий в виде экзмемпляра класса VacanciesHandler"""
        pass

    @abstractmethod
    def convert_params_user_to_api(self, user_search_params: dict) -> dict:
        """Преобразует пользовательские параметры в формат, подходящий для API"""
        pass

    @abstractmethod
    def convert_town_to_number(self, town):
        """Преобразует текстовое название региона в id согласно спецификации API"""
        pass

    @abstractmethod
    def convert_response_to_vacancies(self, response):
        """Преобразует ответ, полученный от API, в список вакансий,
         представленный в виде экземпляра класса VacanciesHandler"""
        pass
