from parser_vacancies.classes.vacancy import Vacancy


class VacanciesHandler:
    """Класс для обработки списка вакансий"""

    def __init__(self, vacansies=[]):
        self.vacancies = vacansies

    def __iter__(self):
        """делаем класс итерируемым"""
        self.__counter = -1
        return self

    def __next__(self):
        """переход к следующему элемменту при итерации"""
        self.__counter += 1

        if self.__counter < len(self.vacancies):
            return self.vacancies[self.__counter]

        raise StopIteration

    def __str__(self):
        """печать экземпляра класса"""
        result = ''
        for vacancy in self.vacancies:
            result += str(vacancy)
        return result

    def sort_by_payment(self):
        """сортирует элементы по ЗП: от большей к меньшей"""
        self.vacancies.sort(key=lambda vacancy: vacancy.payment_for_sort, reverse=True)

    def sort_by_date(self):
        """сортирует элементы по дате публикации вакансий: от новых к старым"""
        self.vacancies.sort(key=lambda vacancy: vacancy.date_published, reverse=True)

    def filter_by_keyword(self, keyword):
        """фильтрует список вакансий, оставляя только те, в названии или описании которых есть слово keword"""
        new_vacancies = []
        for vacancy in self.vacancies:
            if keyword in vacancy.title + vacancy.description:
                new_vacancies.append(vacancy)
        self.vacancies = new_vacancies

    def filter_by_site(self, site):
        """фильтрует список вакансий, оставляя только те, которые пришли с site (hh | sj)"""
        new_vacancies = []
        for vacancy in self.vacancies:
            if vacancy.vacancy_id[:2] == site:
                new_vacancies.append(vacancy)
        self.vacancies = new_vacancies

    def filter_by_distant_work(self):
        """фильтрует список вакансий, оставляя только c возможностью удаленной работы"""
        new_vacancies = []
        for vacancy in self.vacancies:
            if vacancy.distant_work:
                new_vacancies.append(vacancy)
        self.vacancies = new_vacancies

    def print_first_N_in_console(self, count):
        """выводит первые count вакансий или все, если count больше количества вакансий"""
        # проверка корректности полученных данных
        try:
            if count <= 0:
                return
        except Exception:
            return

        # вывод данных
        num = 0
        for vacancy in self.vacancies:
            print(vacancy)
            num += 1
            if num == count:
                break

    def delete_vacancy_by_id(self, vacancy_id):
        """удаляет вакансию по переданному id из списка. Если вакансии с таким id не найдено, ничего не меняет"""
        for vacancy in self.vacancies:
            print("1")
            if vacancy.vacancy_id == vacancy_id:
                self.vacancies.remove(vacancy)
                break

    def replace(self, vacancies):
        """полностью меняет список вакансий на новый"""
        self.vacancies = vacancies

    def extend(self, vacancies):
        """добавляет в список вакансий другой список"""
        self.vacancies.extend(vacancies)

    def append(self, vacancy):
        """добавляет одну вакаесияю в список вакансий"""
        self.vacancies.append(vacancy)


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

# print(str(vacancies))
# vacancies.replace([vacancy3, vacancy1])
# vacancies.extend([vacancy2, vacancy2])
# for vacancy in vacancies:
#     print(vacancy)
