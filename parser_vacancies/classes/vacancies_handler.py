from datetime import datetime, timedelta


class VacanciesHandler:
    """Класс для работы со списком вакансий"""

    def __init__(self, vacansies):
        """Инициализация класса списком."""
        self.vacancies = vacansies

    def __iter__(self):
        """Делаем класс итерируемым"""
        self.__counter = -1
        return self

    def __next__(self):
        """Переход к следующему элементу при итерации"""
        self.__counter += 1

        if self.__counter < len(self.vacancies):
            return self.vacancies[self.__counter]

        raise StopIteration

    def __str__(self):
        """Печать экземпляра класса"""
        result = ''
        for vacancy in self.vacancies:
            result += str(vacancy)
        return result

    def __len__(self):
        """Длина экземпляра класса"""
        return len(self.vacancies)

    def sort_by_payment(self):
        """Сортирует элементы по ЗП: от большей к меньшей"""
        self.vacancies.sort(key=lambda vacancy: vacancy.payment_for_sort, reverse=True)

    def sort_by_date(self):
        """Сортирует элементы по дате публикации вакансий: от новых к старым"""
        self.vacancies.sort(key=lambda vacancy: vacancy.date_published, reverse=True)

    def filter_by_town(self, town):
        """Фильтрует список вакансий, оставляя только те, расположение которых совпадает с town"""
        new_vacancies = []
        town = town.lower()
        for vacancy in self.vacancies:
            if vacancy.town.lower() == town:
                new_vacancies.append(vacancy)
        self.vacancies = new_vacancies

    def filter_by_keyword(self, keyword):
        """Фильтрует список вакансий, оставляя только те,
         в названии или описании которых есть слово keyword"""
        new_vacancies = []
        keyword = keyword.lower().strip()
        for vacancy in self.vacancies:
            if keyword in vacancy.title.lower() + vacancy.description.lower():
                new_vacancies.append(vacancy)
        self.vacancies = new_vacancies

    def filter_by_payment(self, payment):
        """Фильтрует список вакансий, оставляя только те,
        в которых payment входит в вилку ЗП или ЗП не указана"""
        new_vacancies = []
        for vacancy in self.vacancies:
            payment_key = True
            if vacancy.payment_from is not None:
                if vacancy.payment_from > payment:
                    payment_key = False
            if vacancy.payment_to is not None:
                if vacancy.payment_to < payment:
                    payment_key = False
            if payment_key:
                new_vacancies.append(vacancy)
        self.vacancies = new_vacancies

    def filter_only_with_payment(self):
        """Фильтрует список вакансий, оставляя только те, в которых указана ЗП"""
        new_vacancies = []
        for vacancy in self.vacancies:
            if vacancy.payment_from is not None or vacancy.payment_to is not None:
                new_vacancies.append(vacancy)
        self.vacancies = new_vacancies

    def filter_by_distant_work(self):
        """Фильтрует список вакансий, оставляя только c возможностью удаленной работы"""
        new_vacancies = []
        for vacancy in self.vacancies:
            if vacancy.distant_work:
                new_vacancies.append(vacancy)
        self.vacancies = new_vacancies

    def filter_by_day_from(self, day_from):
        """Фильтрует список вакансий, оставляя только те,
        которые опубликованы не более day_from дней назад"""
        new_vacancies = []
        date_from = datetime.today() - timedelta(days=day_from)
        date_from = date_from.isoformat()
        for vacancy in self.vacancies:
            if vacancy.date_published >= date_from:
                new_vacancies.append(vacancy)
        self.vacancies = new_vacancies

    def print_first_N_in_console(self, count):
        """Выводит первые count вакансий или все, если count больше количества вакансий"""
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
        """Удаляет вакансию по переданному id из списка.
        Если вакансии с таким id не найдено, ничего не меняет"""
        for vacancy in self.vacancies:
            print("1")
            if vacancy.vacancy_id == vacancy_id:
                self.vacancies.remove(vacancy)
                break

    def replace(self, vacancies):
        """Полностью меняет список вакансий на новый"""
        self.vacancies = vacancies

    def remove(self):
        """Очищает список вакансий"""
        self.vacancies = []

    def extend(self, new_vacancies):
        """Добавляет в список вакансий другой список"""
        try:
            self.vacancies.extend(new_vacancies.vacancies)
        except Exception:
            pass

    def append(self, vacancy):
        """Добавляет одну вакансию в список вакансий"""
        self.vacancies.append(vacancy)
