class Vacancy:
    """Класс для работы с одной вакансией"""
    def __init__(self, vacancy_id, title, url, description,
                 payment_from, payment_to, distant_work,
                 date_published, town):
        """Инициализация вакансии данными"""
        self.vacancy_id = vacancy_id
        self.title = title
        self.url = url
        self.description = description
        self.payment_from = payment_from
        self.payment_to = payment_to
        self.distant_work = distant_work
        self.date_published = date_published
        self.town = town
        self.payment_for_sort = self.get_payment_for_sort()

    def __repr__(self):
        return f'Vacancy(vacancy_id={self.vacancy_id},\n' \
               f'        title={self.title},\n' \
               f'        url={self.url},\n' \
               f'        description={self.description},\n' \
               f'        payment_from={self.payment_from},\n' \
               f'        payment_to={self.payment_to},\n' \
               f'        distant_work={self.distant_work},\n' \
               f'        date_published={self.date_published},\n' \
               f'        town={self.town})'

    def __str__(self):
        """Печать экземпляра класса"""
        vacancy_text = f'--------------------------\n' \
                       f'{self.title}\n' \
                       f'Ссылка: {self.url}\n' \
                       f'Описание: {self.description[:50]}…\n'
        if self.payment_from is not None:
            payment_from = self.payment_from
        else:
            payment_from = '—'
        if self.payment_to is not None:
            payment_to = self.payment_to
        else:
            payment_to = '—'
        vacancy_text += f'ЗП от {payment_from} до {payment_to}\n' \
                        f'Работа в городе {self.town}\n'
        if self.distant_work:
            vacancy_text += 'Есть возможность удаленной работы\n'
        vacancy_text += f'Дата публикации {self.date_published}\n' \
                        f'--------------------------'
        return vacancy_text

    def short_str(self):
        """Короткая версия метода str для вывода вакансии в консоль"""
        vacancy_text = f'--------------------------\n'\
                       f'{self.title}\n' \
                       f'Ссылка: {self.url}\n'
        if self.payment_from is not None:
            payment_from = self.payment_from
        else:
            payment_from = '—'
        if self.payment_to is not None:
            payment_to = self.payment_to
        else:
            payment_to = '—'
        vacancy_text += f'ЗП от {payment_from} до {payment_to}\n' \
                        f'Дата публикации {self.date_published}\n' \
                        f'--------------------------'
        return vacancy_text

    def get_payment_for_sort(self):
        """Расчет ЗП для сортировки вакансий по ЗП.
        Отталкиваемся от бОльшей ЗП, если ее нет – то переходим к минимальной.
        Если и ее нет – устанавливаем 0"""

        if self.payment_to is not None:
            return self.payment_to
        elif self.payment_from is not None:
            return self.payment_from
        else:
            return 0
