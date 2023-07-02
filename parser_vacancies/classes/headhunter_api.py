from datetime import timedelta, datetime

import requests

from parser_vacancies.classes.job_sites_api import JobSitesAPI
from parser_vacancies.classes.vacancies_handler import VacanciesHandler
from parser_vacancies.classes.vacancy import Vacancy


class HeadHunterAPI(JobSitesAPI):
    """Класс для работы с HeadHunter API"""
    def __init__(self):
        """Инициализация HH_API, задаем headers и базовый url для работы с API"""
        self._request_headers = {'HH-User-Agent': 'parser_vacancies/1.0 (a.kolmychek@gmail.com)',
                                 'Connection': 'close',
                                 }
        self._request_url = 'https://api.hh.ru/'

    # Подсказка по используемым параметрам поиска в API
    # self._params = {'area': None,  # место расположения офиса
    #                 'text': None,  # ключевые слова поиска
    #                 'schedule': None,  # удаленная работа = 'remote'
    #                 'salary': None,  # желаемая зп
    #                 'only_with_salary': False,  # True = только с указанием ЗП
    #                 'date_from': None,  # вакансии опубликованы с даты (ISO 8601 - YYYY-MM-DD)
    #                 'per_page': 100,  # максимальное количество вакансий
    #                 }

    def get_vacancies(self, user_search_params: dict) -> VacanciesHandler:
        """Получает по API вакансии с заданными параметрами,
           возвращает список вакансий в виде экзмемпляра класса VacanciesHandler"""
        api_search_params = self.convert_params_user_to_api(user_search_params)
        response = requests.get(self._request_url + 'vacancies',
                                headers=self._request_headers,
                                params=api_search_params)
        vacancies = self.convert_response_to_vacancies(response)
        return vacancies

    def convert_params_user_to_api(self, user_search_params: dict) -> dict:
        """Преобразует пользовательские параметры в формат, подходящий для API"""

        # поиск на 100 вакансий - максимальное значение за раз
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

        # задаем фильтр – вакансии только с ЗП
        if user_search_params.get('only_with_payment') is not None:
            api_search_params['only_with_salary'] = user_search_params['only_with_payment']

        # задаем фильтр – вакансии только с удаленной работой - для HH работает не совсем корректно
        if user_search_params.get('distant_work') is not None:
            if user_search_params['distant_work']:
                api_search_params['schedule'] = 'remote'

        # задаем начальную дату публикации вакансий
        if user_search_params.get('day_from') is not None:
            date_from = datetime.today() - timedelta(days=user_search_params['day_from'])
            api_search_params['date_from'] = date_from.isoformat()

        return api_search_params

    def convert_town_to_number(self, town):
        """Преобразует текстовое название региона в id согласно словарю API.
        Работаем только в России, при желании можно расширить"""

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
        """Рекурсивная функция для поиска региона на всех уровнях вложения словаря.
        Специфично для HeadHunter API"""
        name = name.title()
        for item in data:
            if item['name'] == name:
                return item['id']
            elif len(item['areas']) != 0:
                town_id = self.get_area_id(item['areas'], name)
                if town_id is not None:
                    return town_id

    def convert_response_to_vacancies(self, response):
        """Преобразует ответ, полученный от API, в список вакансий,
         представленный в виде экземпляра класса VacanciesHandler"""
        try:
            response = response.json()['items']
        except Exception:
            return []
        vacancies = VacanciesHandler([])
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

