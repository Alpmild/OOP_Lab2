import pandas
from time import time
from os.path import exists, splitext
from sys import stdin

expansions = ('.xml', '.csv')


class Table:
    def __init__(self, table):
        self.__table = table

    def get(self):
        return self.__table

    def add(self, other):
        self.__table = self.__table._append(other.get())

    def count(self, column, value, drop_dup=True):
        frame = self.__table[self.__table[column] == value]
        if drop_dup:
            frame = frame.drop_duplicates()
        return len(frame)

    def duplicates(self):
        repeats = self.__table.value_counts().reset_index(name='count')
        repeats = repeats[repeats['count'] > 1]
        return Table(repeats)


def process(directory: str):
    if not exists(directory):
        print('Файл не существует')
        return
    expan = splitext(directory)[1]
    if expan not in expansions:
        print('Файл не поддерживается')
        return

    match expan:
        case '.csv':
            main_table = Table(pandas.read_csv(directory, sep=';', header=0))
        case '.xml':
            main_table = Table(pandas.read_xml(directory))
    repeats = Table(pandas.DataFrame(columns=tuple(main_table.get().columns) + ('count',)))

    cities = main_table.get()['city'].drop_duplicates()
    for city in cities:
        print(f'{city}:')
        city_table = Table(main_table.get()[main_table.get()['city'] == city])
        for f in range(1, 6):
            print(f'\t{f}: {city_table.count("floor", f)}')
        print()
        repeats.add(city_table.duplicates())

    print("Повторные записи:", repeats.get(), sep='\n')


def main():
    print("Директория файла: ", end='')
    for dir in stdin:
        start = time()
        process(str(dir)[:-1])
        print(f'\nВремя обработки файла: {round(time() - start, 3)} сек.')

        print("\nДиректория файла: ", end='')


main()
