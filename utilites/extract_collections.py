from pandas import DataFrame
import gc
import re
from re import Pattern

from settings import src_model, service_data, console_colors, Collection
from .get_duplicates import get_duplicates


def get_collection_data(row: int, df: DataFrame) -> Collection:
    """ Получает данные о Сборнике из df на строке row.
        Возвращает кортеж:
            - номер строки в исходном файле. Он совпадает с индексом.
            - код главы
            - код сборника
            - номер сборника из названия
            - название
    """
    index = df.index[row]
    chapter_cod = df.at[index, src_model['глава']['column_name']].strip()
    collection_code = str(df.at[index, src_model['сборник']['column_name']]).strip()
    collection_field = df.at[index, src_model['заголовок']['column_name']].split()
    collection_number = collection_field[1][:-1]
    collection_title = " ".join(collection_field[2:])
    return Collection(
        row=index, chapter_code=chapter_cod, code=collection_code,
        number=collection_number, title=collection_title
    )


def try_repair(collection: tuple[int, str, str, str, str], pattern: Pattern) -> tuple | None:
    """ Пытается починить строку Сборника, если у нее кривой код.
        Собирает новый код из кода Главы + номер сборника из названия Сборника.
        collection - строка сборника.
        Возвращает отремонтированную строку Сборника либо None.
    """
    collection_code_position = 2
    cod_new = f"{collection[collection_code_position-1]}.{collection[collection_code_position+1]}"
    if pattern.fullmatch(cod_new):
        tmp = list(collection)
        tmp[collection_code_position] = cod_new
        # tuple(item for item in tmp)
        return (*tmp,)
    return None


def collections_extract(df: DataFrame):
    """ Извлекает Сборники из df и формирует словарь Сборников в общем хранилище service_data['collections'].
        df -  без пустых значений в столбце 'H', столбцы ['B', 'C', 'D', 'E', 'F', 'H'] pandas dataframe.
    """
    column_name = src_model['заголовок']['column_name']
    re_collection_title = src_model['сборник']['title_pattern']
    print(f"Сборник: столбец заголовка {column_name!r}, шаблон для поиска: {re_collection_title!r}", )

    collections_df = df[df[column_name].str.contains(re_collection_title, case=False, regex=True)]
    collections = [get_collection_data(row, collections_df) for row in range(collections_df.shape[0])]
    print('Сборники:', len(collections))

    re_code = re.compile(src_model['сборник']['code_pattern'])
    collection_code_position = 2
    bug_collections = {i: x for i, x in enumerate(collections) if re_code.fullmatch(x[collection_code_position]) is None}
    if len(bug_collections) > 0:
        repaired = {key: rep_i for key, value in bug_collections.items() if (rep_i := try_repair(value, re_code))}
        print(f"отремонтированные Сборники: {repaired}")
        if len(repaired) > 0:
            for key in repaired.keys():
                collections[key] = repaired[key]
                bug_collections.pop(key, None)
        print(f"кривые 'Сборники': {console_colors['YELLOW']}{bug_collections}{console_colors['RESET']}")
    service_data['collections'].update({x[collection_code_position]: x for x in collections})

    if len(service_data['collections']) != len(collections):
        duplicates = get_duplicates([x[collection_code_position] for x in collections])
        error_out = f"Есть дубликаты 'Отделов': {console_colors['RED']}{duplicates}{console_colors['RESET']}"
        print(error_out)

    del collections_df
    gc.collect()
