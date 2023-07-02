# TODO взаимодействие с пользователем через консоль
#  позволет пользователю указать, с каких платформ он хочет получить вакансии,
#  ввести поисковый запрос,
#  получить топ N вакансий по зарплате,
#  получить вакансии в отсортированном виде,
#  получить вакансии, в описании которых есть определенные ключевые слова, например "postgres" и т. п.
import os.path
from os import listdir
from os.path import isfile

from parser_vacancies.classes.excel_file_handler import ExcelFileHandler
from parser_vacancies.classes.headhunter_api import HeadHunterAPI
from parser_vacancies.classes.json_file_handler import JSONFileHandler
from parser_vacancies.classes.superjob_api import SuperJobAPI
from parser_vacancies.classes.vacancies_handler import VacanciesHandler
from parser_vacancies.constants import DATA_DIR

vacancies = VacanciesHandler([])


# user_filter_params = {'town': str,
#                       'keywords': str,
#                       'payment': int,
#                       'only_with_payment': bool,
#                       'distant work': bool,
#                       'day_from': int,
#                       }

def user_interaction():
    show_rules()
    while True:
        action = get_user_action()
        if action == '1':
            get_vacancies()
        elif action == '2':
            filter_vacancies()
        elif action == '3':
            sort_vacancies()
        elif action == '4':
            print_vacancies()
        elif action == '5':
            write_vacancies_in_file()
        elif action == '6':
            remove_vacancies()


def get_user_action():
    if len(vacancies) == 0:
        user_input = input('\nСписок вакансий пуст. Хотите получить вакансии? (да/нет) ').lower()
        if user_input == 'да':
            user_input = '1'
        elif user_input != 'выход':
            user_input = '0'
    else:
        user_input = input('\nВыберите действие:\n'
                           '1 - получить список вакансий\n'
                           '2 - отфильтровать вакансии\n'
                           '3 - отсортировать вакансии\n'
                           '4 - вывести вакансии на экран\n'
                           '5 - записать вакансии в файл\n'
                           '6 - очистить список вакансий\n')

    check_exit(user_input)
    if user_input not in ['1', '2', '3', '4', '5', '6']:
        print('-' * 10, 'Некорректный ввод', '-' * 10)

    return user_input


def show_rules():
    print('Для завершения работы в любой момент введите слово "выход".')
    print('Для пропуска ввода параметров поиска или использования значений по умолчанию нажмите Enter.')


def check_exit(user_input):
    if user_input.lower() == 'выход':
        exit()


def get_vacancies():
    global vacancies
    if len(vacancies) != 0:
        user_input = input('\nСписок вакансий не пустой. Очистить перед добавлением? (да/нет) ').lower().strip()
        if user_input == 'да':
            remove_vacancies()
    vacancies_place = get_vacancies_place()
    if vacancies_place is not None:
        params = get_filter_params('123456')
        vacancies_place = set(vacancies_place)
        for num in vacancies_place:
            temp_vacancies = []
            if num == '1':
                temp_vacancies = get_vacancies_from_hh(params)
                platform_name = ['c HH', 'На HH']
            elif num == '2':
                temp_vacancies = get_vacancies_from_sj(params)
                platform_name = ['c JS', 'На JS']
            elif num == '3':
                temp_vacancies = get_vacancies_from_file(params)
                platform_name = ['из файла', 'В файле']

            if num in '123':
                if len(temp_vacancies) != 0:
                    print('-' * 10, f'Вакансии {platform_name[0]} получены', '-' * 10)
                else:
                    print('-' * 10, f'{platform_name[1]} не найдено подходящих вакансий', '-' * 10)
            vacancies.extend(temp_vacancies)


def filter_vacancies():
    global vacancies
    user_filters = get_filters()
    if set(user_filters) & set('123456') != set():
        user_filter_params = get_filter_params(user_filters)
        vacancies = filter_vacancies_by_params(vacancies, user_filter_params)
        print('-' * 10, 'Вакансии отфильтрованы', '-' * 10)
    else:
        print('-' * 10, 'Некорректный ввод', '-' * 10)


def sort_vacancies():
    global vacancies
    sort_param = get_sort_param()
    if sort_param == '1':
        vacancies.sort_by_payment()
        print('-' * 10, 'Вакансии отсортированы', '-' * 10)
    elif sort_param == '2':
        vacancies.sort_by_date()
        print('-' * 10, 'Вакансии отсортированы', '-' * 10)
    else:
        print('-' * 10, 'Некорректный ввод', '-' * 10)


def print_vacancies():
    user_count = input('\nСколько вакансий вывести?\n'
                       'Для вывода всех вакансий нажмите Enter\n')
    check_exit(user_count)
    try:
        user_count = int(user_count)
        vacancies.print_first_N_in_console(user_count)
        count = min(user_count, len(vacancies))
        print(f'\nВсего вакансий: {len(vacancies)}. Выведено вакансий: {count}')
    except ValueError:
        print(vacancies,
              f'\nВсего вакансий: {len(vacancies)}')

    print('-' * 10, 'Вакансии выведены', '-' * 10)


def write_vacancies_in_file():
    while True:
        user_file_name = input('Введите имя файла с расширением '
                               'или "отмена" для продолжения работы: ').lower().strip()

        check_exit(user_file_name)

        if user_file_name == 'отмена':
            return None

        if user_file_name.endswith('.json'):
            file_name = user_file_name[:-5]
            file_handler = JSONFileHandler(file_name)
            break
        elif user_file_name.endswith('.xlsx'):
            file_name = user_file_name[:-5]
            file_handler = ExcelFileHandler(file_name)
            break
        else:
            print('Поддерживаются только файлы .json или .xlsx')
            continue
    if file_handler.is_file_exist():
        user_input = input('Такой файл уже существует\n'
                           'Очистить файл перед записью? (да/нет) ').lower().strip()
        check_exit(user_input)
        if user_input == 'да':
            file_handler.overwrite_vacancies(vacancies)
        else:
            file_handler.add_vacancies(vacancies)
    else:
        file_handler.overwrite_vacancies(vacancies)
    print('-' * 10, f'Работа с файлом {user_file_name} завершена', '-' * 10)


def remove_vacancies():
    global vacancies
    vacancies.remove()
    print('-' * 10, 'Список вакансий очищен', '-' * 10)


def get_vacancies_place():
    vacancies_place = input('\nОткуда будем загружать вакансии?\n'
                            'Чтобы совместить выбор, введите нужные номера без пробелов и знаков препинания.\n'
                            '1 - HeadHunter.ru; 2 – SuperJob.ru; 3 - из файла\n')
    check_exit(vacancies_place)
    if set(vacancies_place) & set('123') == set():
        print('-' * 10, 'Некорректный ввод', '-' * 10)
        return None
    else:
        return vacancies_place


def get_filter_params(filters):
    # user_filter_params = {'1-town': str,
    #                       '2-keywords': str,
    #                       '3-payment': int,
    #                       '4-only_with_payment': bool,
    #                       '5-distant_work': bool,
    #                       '6-day_from': int,
    #                       }
    user_filter_params = {}

    for item in filters:
        if item == '1':
            town = input('В каком городе искать вакансии? ')
            check_exit(town)
            if town != '':
                user_filter_params['town'] = town

        if item == '2':
            keywords = input('Ключевые слова для поиска: ')
            check_exit(keywords)
            if keywords != '':
                user_filter_params['keywords'] = keywords

        if item == '3':
            payment = input('Ожидаемая зарплата: ')
            check_exit(payment)
            if payment != '':
                try:
                    user_filter_params['payment'] = int(payment)
                except ValueError:
                    print('Ввод не корректен, поиск будет осуществляться без учета этого параметра.')

        if item == '4':
            only_with_payment = input('Только вакансии с указанием ЗП (да/нет): ')
            check_exit(only_with_payment)
            if only_with_payment != '':
                if only_with_payment == 'да':
                    user_filter_params['only_with_payment'] = True
                # elif only_with_payment == 'нет':
                #     user_filter_params['only_with_payment'] = False

        if item == '5':
            distant_work = input('Только удаленная работа (да/нет): ')
            check_exit(distant_work)
            if distant_work != '':
                if distant_work != '':
                    if distant_work == 'да':
                        user_filter_params['distant_work'] = True
                    # elif distant_work == 'нет':
                    #     user_filter_params['distant_work'] = False

        if item == '6':
            day_from = input('За сколько последних дней показать вакансии? ')
            check_exit(day_from)
            if day_from != '':
                try:
                    user_filter_params['day_from'] = int(day_from)
                except ValueError:
                    print('Ввод не корректен, поиск будет осуществляться без учета этого параметра.')

    return user_filter_params


def get_vacancies_from_hh(params):
    hh_api = HeadHunterAPI()
    hh_vacancies = hh_api.get_vacancies(params)
    return hh_vacancies


def get_vacancies_from_sj(params):
    sj_api = SuperJobAPI()
    sj_vacancies = sj_api.get_vacancies(params)
    return sj_vacancies


def get_vacancies_from_file(params):
    file_handler = get_file_for_read()
    if file_handler is not None:
        file_vacancies = file_handler.read_vacancies()
        file_vacancies = filter_vacancies_by_params(file_vacancies, params)
        return file_vacancies
    return []

def get_file_for_read():
    is_good_file = False
    while not is_good_file:
        user_file_name = input('Введите имя файла с расширением '
                               'или "отмена" для продолжения работы: ').lower().strip()

        check_exit(user_file_name)

        if user_file_name == 'отмена':
            break

        if user_file_name.endswith('.json'):
            file_name = user_file_name[:-5]
            file_handler = JSONFileHandler(file_name)
        elif user_file_name.endswith('.xlsx'):
            file_name = user_file_name[:-5]
            file_handler = ExcelFileHandler(file_name)
        else:
            print('Поддерживаются только файлы .json или .xlsx')
            continue
        is_good_file = file_handler.is_file_exist()
        if not is_good_file:
            need_file_list = input('Такого файла нет\n'
                                   'Вывести список доступных файлов? (да/нет) ')
            check_exit(need_file_list)
            if need_file_list == 'да':
                print_files_list()

    if is_good_file:
        return file_handler
    else:
        return None

def print_files_list():
    files_list = [f for f in listdir(DATA_DIR) if f.endswith('.json') or f.endswith('.xlsx')]
    if len(files_list) == 0:
        print('Доступных файлов нет')
    else:
        files_list = '    '.join(files_list)
        print(files_list)


def filter_vacancies_by_params(vacancies_to_filter, params):
    if params.get('town') is not None:
        vacancies_to_filter.filter_by_town(params['town'])
    if params.get('keywords') is not None:
        vacancies_to_filter.filter_by_keyword(params['keywords'])
    if params.get('payment') is not None:
        vacancies_to_filter.filter_by_payment(params['payment'])
    if params.get('only_with_payment') is not None:
        vacancies_to_filter.filter_only_with_payment()
    if params.get('distant_work') is not None:
        vacancies_to_filter.filter_by_distant_work()
    if params.get('day_from') is not None:
        vacancies_to_filter.filter_by_day_from(params['day_from'])
    return vacancies_to_filter


def get_filters():
    filters = input('\nВыберите параметр, по которым хотите отфильтровать вакансии.\n'
                    'Чтобы совместить выбор, введите нужные номера без пробелов и знаков препинания.\n'
                    '1 - город работы\n'
                    '2 - ключевое слово\n'
                    '3 - размер ЗП\n'
                    '4 - указание ЗП\n'
                    '5 - возможность дистанционной работы\n'
                    '6 - дата публикации\n')
    check_exit(filters)
    return filters

def get_sort_param():
    sort_param = input('\nВыберите параметр, по которому будем сортировать вакансии.\n'
                    '1 - по ЗП (от большей к меньшей)\n'
                    '2 - по дате публикации (от новых к старым)\n')
    check_exit(sort_param)
    return sort_param


# get_vacancies_from_file([])
user_interaction()
