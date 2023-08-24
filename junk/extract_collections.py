from pandas import DataFrame
import gc
import re
from re import Pattern

from settings import src_model, service_data, console_colors, Collection
from utilites.get_duplicates import get_duplicates


def get_collection_data(row: int, df: DataFrame) -> Collection:
    """ Получает данные о Сборнике из df на строке row.
        Возвращает экземпляр класса Collection:
    """
    index = df.index[row]
    chapter_code = df.at[index, src_model['глава']['column_name']].strip()
    code = str(df.at[index, src_model['сборник']['column_name']]).strip()
    field = df.at[index, src_model['заголовок']['column_name']].split()
    number = field[1][:-1]
    title = " ".join(field[2:])
    return Collection(row=index, chapter_code=chapter_code, code=code, number=number, title=title)


def repair_collection_code(collection: Collection, pattern: Pattern) -> bool:
    """ Пытается починить код Сборника. Собирает новый код из кода Главы + номер_сборника из названия Сборника.
    """
    new_code = f"{collection.chapter_code}.{collection.number}"
    if pattern.fullmatch(new_code):
        collection.code = new_code
        return True
    return False


def collections_extract(df: DataFrame):
    """ Извлекает Сборники из df и формирует словарь Сборников в общем хранилище service_data['collections'].
        df -  без пустых значений в столбце 'H', столбцы ['B', 'C', 'D', 'E', 'F', 'H'] pandas dataframe.
    """
    column_name = src_model['заголовок']['column_name']
    re_collection_title = src_model['сборник']['title_pattern']
    print(f"Сборник: столбец заголовка {column_name!r}, шаблон для поиска: {re_collection_title!r}", )
    # выделяем строки похожие на Сборники из df
    collections_df = df[df[column_name].str.contains(re_collection_title, case=False, regex=True)]
    collections = [get_collection_data(row, collections_df) for row in range(collections_df.shape[0])]
    print('Сборники:', len(collections))
    # проверяем коды полученных сборников и кривые записываем в список
    re_code = re.compile(src_model['сборник']['code_pattern'])
    bug_collections = {i: x for i, x in enumerate(collections) if re_code.fullmatch(x.code) is None}
    if len(bug_collections) > 0:
        print(f"кривые 'Сборники': {console_colors['YELLOW']}{bug_collections}{console_colors['RESET']}")
        # пытаемся ремонтировать коды сборников
        repaired = {key: value for key, value in bug_collections.items() if repair_collection_code(value, re_code)}
        print(f"отремонтированные Сборники: {repaired}")
        if len(repaired) > 0:
            for key in repaired.keys():
                collections[key] = repaired[key]
                bug_collections.pop(key, None)
        print(f"кривые 'Сборники': {console_colors['YELLOW']}{bug_collections}{console_colors['RESET']}")
    service_data['collections'].update({x.code: x for x in collections})
    # проверяем на Сборники с одинаковым кодом
    if len(service_data['collections']) != len(collections):
        duplicates = get_duplicates([x.code for x in collections])
        error_out = f"Есть дубликаты 'Сборников': {console_colors['RED']}{duplicates}{console_colors['RESET']}"
        print(error_out)

    del collections_df
    gc.collect()
