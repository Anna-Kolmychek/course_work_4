import json
import os
from datetime import datetime, timedelta
import time

import requests

from parser_vacancies.classes.job_sites_api import JobSitesAPI
from parser_vacancies.classes.vacancies_handler import VacanciesHandler
from parser_vacancies.classes.vacancy import Vacancy


class SuperJobAPI(JobSitesAPI):
    def __init__(self):
        """Инициализация SJ_API, задаем headers и базовый url для работы с API
        ключ для headers берем из системный переменных"""
        self._request_headers = {'X-Api-App-Id': os.getenv('SECRET_KEY_SUPER_JOB_API'),
                                 'Connection': 'close',
                                 }
        self._request_url = 'https://api.superjob.ru/2.0/'
        # Подсказка по параметрам поиска в API
        # self._params = {'town': None,  # место расположения
        #                 'keywords': None,  # ключевые слова поиска
        #                 'place_of_work': None,  # место работы: 2 - на дому
        #                 'payment_from': None,  # ЗП от
        #                 'no_agreement': None,  # 1 – только с указанием ЗП
        #                 'date_published_from': None,  # вакансии опубликованы с даты (unixtime)
        #                 'count': 100,  # максимальное количество вакансий
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
        api_search_params = {'count': 100}

        # задаем расположение (преобразуем текст в id)
        if user_search_params.get('town') is not None:
            town_id = self.convert_town_to_number(user_search_params['town'])
            if town_id is not None:
                api_search_params['town'] = town_id
            else:
                api_search_params['town'] = -1

        # задаем ключевые слова
        if user_search_params.get('keywords') is not None:
            api_search_params['keywords'] = user_search_params['keywords']

        # задаем ЗП
        if user_search_params.get('payment') is not None:
            api_search_params['payment_from'] = user_search_params['payment']

        # задаем фильтр: вакансии только с ЗП
        if user_search_params.get('only_with_payment') is not None:
            if user_search_params['only_with_payment']:
                api_search_params['no_agreement'] = 1

        # задаем фильтр: вакансии только с удаленной работой
        if user_search_params.get('distant_work') is not None:
            if user_search_params['distant_work']:
                api_search_params['place_of_work'] = 2

        # задаем начальную дату публикации вакансий
        if user_search_params.get('day_from') is not None:
            date_from = datetime.today() - timedelta(days=user_search_params['day_from'])
            api_search_params['date_published_from'] = time.mktime(date_from.timetuple())

        return api_search_params

    def convert_town_to_number(self, name):
        """переводит текстовое название города или региона в id согласно слорю"""
        name = name.title()
        # Ищем в регионах
        response = requests.get(self._request_url + 'regions/?keyword=' + name,
                                headers=self._request_headers)
        for item in response.json()['objects']:
            if item['title'] == name:
                return item['id']

        # Ищем в городах
        response = requests.get(self._request_url + 'towns/?keyword=' + name,
                                headers=self._request_headers)
        for item in response.json()['objects']:
            if item['title'] == name:
                return item['id']

        return None

    def convert_response_to_vacancies(self, response):
        """Преобразует ответ, полученный от API, в список элементов класса Vacancy"""
        response = response.json()['objects']
        vacancies = VacanciesHandler([])
        for item in response:
            vacancy_id = 'sj' + str(item['id'])
            title = item['profession']
            url = item['link']
            try:
                description = item['candidat'].replace('\n', ' ')
            except Exception:
                description = ''
            if item['payment_from'] == 0:
                payment_from = None
            else:
                payment_from = item['payment_from']
            if item['payment_to'] == 0:
                payment_to = None
            else:
                payment_to = item['payment_to']
            if item['place_of_work']['id'] == 2:
                distant_work = True
            else:
                distant_work = False
            date_published = datetime.fromtimestamp(item['date_published']).strftime('%Y-%m-%d')
            town = item['town']['title']

            vacancy = Vacancy(vacancy_id, title, url, description,
                              payment_from, payment_to, distant_work,
                              date_published, town)
            vacancies.append(vacancy)
        return vacancies


#   РАБОЧЕЕ ДЛЯ ОТЛАДКИ
# user_search_params = {'town': int,
#                       'keywords': str | list,
#                       'payment': int,
#                       'only_with_payment': bool,
#                       'distant work': bool,
#                       'day_from': int,
#                       }
#
sj_api = SuperJobAPI()
# print(sj_api.convert_town_to_number('Московская область'))
# params = {'town': 4,  # место расположения офиса
#           'keywords': None,  # ключевые слова поиска [слово1, слово2]
#           'place_of_work': None,  # 1 — на территории работодателя, 2 — на дому, 3 — разъездного характера
#           'payment_from': None,  # ЗП от
#           'payment_to': None,  # ЗП от
#           'no_agreement': 1,  # только с указанием ЗП
#           'date_published_from': None,  # вакансии с даты (unixtime)
#           'count': 100
#           }
user_search_params = {'town': 'Химки',
                      'keywords': None,
                      'payment': None,
                      'only_with_payment': None,
                      'distant_work': None,
                      'day_from': None,
                      }


# print(json.dumps(sj_api.convert_params_user_to_api(user_search_params), indent=2))
# vacancies = sj_api.get_vacancies(user_search_params)
# for item in vacancies:
#     print(item)
#     print('-' * 50)
# print(json.dumps(vacancies, indent=2, ensure_ascii=False))
# print(len(vacancies))
# print(vacancies[10])
