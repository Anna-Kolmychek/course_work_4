import json
from datetime import timedelta, datetime

import requests

from parser_vacancies.classes.job_sites_api import JobSitesAPI


class HeadHunterAPI(JobSitesAPI):
    def __init__(self):
        """Инициализация HH_API, задаем headers и базовый url для работы с API"""
        self._request_headers = {'HH-User-Agent': 'parser_vacancies/1.0 (a.kolmychek@gmail.com)',
                                 'Connection': 'close',
                                 }
        self._request_url = 'https://api.hh.ru/'

    # Подсказка по параметрам поиска в API
    # self._params = {'area': None,  # место расположения офиса
    #                 'text': None,  # ключевые слова поиска
    #                 'schedule': None,  # удаленная работа = 'remote'
    #                 'salary': None,  # желаемая зп
    #                 'only_with_salary': False,  # True = только с указанием ЗП
    #                 'date_from': None,  # вакансии опубликованы с даты (ISO 8601 - YYYY-MM-DD)
    #                 'per_page': 100,  # максимальное количество вакансий
    #                 }

    def get_vacancies(self, user_search_params: dict) -> list | None:
        """Получает по api вакансии по заданным параметрам,
           возвращает список из элементов класса Vacancy"""
        api_search_params = self.convert_params_user_to_api(user_search_params)
        response = requests.get(self._request_url + 'vacancies',
                                headers=self._request_headers,
                                params=api_search_params)
        vacancies = self.convert_response_to_vacancies(response)
        return vacancies

    @staticmethod
    def convert_params_user_to_api(user_search_params: dict) -> dict:
        """Преобразует пользовательские параметры в формат, подходящий для API"""

        # поиск на 100 вакансий
        api_search_params = {'per_page': 100}

        # задаем расположение (по id)
        if user_search_params.get('town') is not None:
            api_search_params['area'] = user_search_params['town']

        # задаем ключевые слова
        if user_search_params.get('keywords') is not None:
            api_search_params['text'] = user_search_params['keywords']

        # задаем ЗП
        if user_search_params.get('payment') is not None:
            api_search_params['salary'] = user_search_params['payment']

        # задаем фильтр: вакансии только с ЗП
        if user_search_params.get('only_with_payment') is not None:
            api_search_params['only_with_salary'] = user_search_params['only_with_payment']

        # задаем фильтр: вакансии только с удаленной работой
        if user_search_params.get('distant_work') is not None:
            if user_search_params['distant_work']:
                api_search_params['schedule'] = 'remote'

        # задаем начальную дату публикации вакансий
        if user_search_params.get('day_from') is not None:
            date_from = datetime.today() - timedelta(days=user_search_params['day_from'])
            api_search_params['date_from'] = date_from.isoformat()

        return api_search_params

    @staticmethod
    def convert_response_to_vacancies(response):
        """Преобразует ответ, полученный от API, в список элементов класса Vacancy"""
        # TODO сделать метод
        pass

#   РАБОЧЕЕ ДЛЯ ОТЛАДКИ
# hh_api = HeadHunterAPI()
# params = {'area': 1,  # место расположения офиса
#           'text': None,  # ключевые слова поиска
#           'schedule': None,  # удаленная работа = 'remote'
#           'salary': None,  # желаемая зп
#           'only_with_salary': True,  # только с указанием ЗП
#           'date_from': None,  # вакансии с даты (ISO 8601 - YYYY-MM-DD)
#           'per_page': 100
#           }
#
# user_search_params = {'town': 1,
#                       'keywords': 'python',
#                       'payment': 50_000,
#                       'only_with_payment': True,
#                       'distant_work': True,
#                       'day_from': 3,
#                       }
# print(json.dumps(hh_api.convert_params_user_to_api(user_search_params), indent=2))
# vacancies = hh_api.get_vacancies(params)
# for item in vacancies['items']:
#     print(json.dumps(item, indent=2, ensure_ascii=False))
#     print('-' * 50)
# print(json.dumps(vacancies, indent=2, ensure_ascii=False))
