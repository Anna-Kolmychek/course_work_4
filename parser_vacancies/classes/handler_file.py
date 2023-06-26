from abc import ABC


class FileHandler(ABC):
    pass
# TODO добавление вакансий в файл

# TODO получение данных из файла по указанным критериям

# TODO удаление информации о вакансиях


class JSONFileHandler(FileHandler):
    pass


class CSVFileHandler(FileHandler):
    pass
