import json
from datetime import timedelta, datetime
from time import sleep

import requests

from parser_vacancies.classes.job_sites_api import JobSitesAPI
from parser_vacancies.classes.vacancy import Vacancy


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

    def convert_params_user_to_api(self, user_search_params: dict) -> dict:
        """Преобразует пользовательские параметры в формат, подходящий для API"""

        # поиск на 100 вакансий
        api_search_params = {'per_page': 100}

        # задаем расположение (преобразуем текст в id)
        if user_search_params.get('town') is not None:
            town_id = self.convert_town_to_number(user_search_params['town'])
            if town_id is not None:
                api_search_params['area'] = town_id
            else:
                api_search_params['area'] = 0


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

    def convert_town_to_number(self, town):
        """переводит текстовое название региона в id согласно слорю api
        работаем только в России, при желании можно расширить"""

        response = requests.get(self._request_url + 'areas/countries',
                                headers=self._request_headers)
        for item in response.json():
            if item['name'] == 'Россия':
                rus_id = item['id']
                break

        response = requests.get(self._request_url + 'areas/' + rus_id,
                                headers=self._request_headers)

        town_id = self.get_area_id(response.json()['areas'], town)
        return town_id

    def get_area_id(self, data, name):
        """рекурсивная функция для поиска региона на всех уровнях вложения"""
        for item in data:
            if item['name'] == name:
                return item['id']
            elif len(item['areas']) != 0:
                town_id = self.get_area_id(item['areas'], name)
                if town_id is not None:
                    return town_id

    def convert_response_to_vacancies(self, response):
        """Преобразует ответ, полученный от API, в список элементов класса Vacancy"""

        try:
            response = response.json()['items']
        except Exception:
            return []
        vacancies = []
        for item in response:
            vacancy_id = 'hh' + item['id']
            title = item['name']
            url = item['alternate_url']
            description = f'Обязанности: ' \
                          f'{item["snippet"]["responsibility"]}' \
                          f'Требования:' \
                          f'{item["snippet"]["requirement"]}'
            try:
                payment_from = item['salary']['from']
                payment_to = item['salary']['to']
            except Exception:
                payment_from = None
                payment_to = None
            if item['schedule'] == 'remote':
                distant_work = True
            else:
                distant_work = False
            date_published = item['published_at'][:10]
            town = item['area']['name']

            vacancy = Vacancy(vacancy_id, title, url, description,
                              payment_from, payment_to, distant_work,
                              date_published, town)
            vacancies.append(vacancy)
        return vacancies

    # def get_vacancy_description(self, vacancy_id):
    #     """Получает полное описание вакансии через запрос к вакансии по id"""
    #     response = requests.get(self._request_url + f'vacancies/{vacancy_id}',
    #                             headers=self._request_headers)
    #     return response.json()['description']


#   РАБОЧЕЕ ДЛЯ ОТЛАДКИ
hh_api = HeadHunterAPI()
# params = {'area': 1,  # место расположения офиса
#           'text': None,  # ключевые слова поиска
#           'schedule': None,  # удаленная работа = 'remote'
#           'salary': None,  # желаемая зп
#           'only_with_salary': True,  # только с указанием ЗП
#           'date_from': None,  # вакансии с даты (ISO 8601 - YYYY-MM-DD)
#           'per_page': 100
#           }
#
user_search_params = {'town': 'Московская область',
                      'keywords': '',
                      'payment': 50_000,
                      'only_with_payment': False,
                      'distant_work': True,
                      'day_from': 1,
                      }
# print(json.dumps(hh_api.convert_params_user_to_api(user_search_params), indent=2))
# vacancies = hh_api.get_vacancies(user_search_params)
# for item in vacancies:
#     print(item)
# print(json.dumps(vacancies, indent=2, ensure_ascii=False))

# request_headers = {'HH-User-Agent': 'parser_vacancies/1.0 (a.kolmychek@gmail.com)',
#                          'Connection': 'close',
#                          }
# request_url = 'https://api.hh.ru/'
#
# response = requests.get(request_url + 'vacancies/82346986',
#                         headers=request_headers)
# print(json.dumps(response.json(),indent=2, ensure_ascii=False))
# hh_api.convert_town_to_number('Московская областьфвыа')
