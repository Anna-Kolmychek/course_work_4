from abc import ABC, abstractmethod


class JobSitesAPI(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_vacancies(self, user_search_params: dict) -> list:
        pass

    @staticmethod
    @abstractmethod
    def convert_params_user_to_api(user_search_params: dict) -> dict:
        pass

    @abstractmethod
    def convert_response_to_vacancies(self, response):
        pass


# TODO подключение к API

# TODO получение вакансий
