from pandas import DataFrame
import gc
from settings import SourceData, src_model, service_data, Collection
import re
from re import Pattern

from pprint import pprint


def get_collection_data(row: int, df: DataFrame) -> tuple[int, str, str, str, str]:
    """ Получает данные о Сборнике из data_frame на строке row.
        Возвращает кортеж:
            - номер строки в исходном файле. Он совпадает с индексом.
            - код главы
            - код сборника
            - номер сборника из названия
            - название
    """
    index = df.index[row]
    chapter_cod = df.at[index, src_model['глава']['column_name']].strip()
    collection_cod = str(df.at[index, src_model['сборник']['column_name']]).strip()
    collection_field = df.at[index, src_model['заголовок']['column_name']].split()
    collection_number = collection_field[1][:-1]
    collection_title = " ".join(collection_field[2:]).capitalize()
    return index, chapter_cod, collection_cod, collection_number, collection_title


def try_repair(collection: tuple[int, str, str, str, str], pattern: Pattern) -> tuple | None:
    cod_new = f"{collection[1]}.{collection[3]}"
    if pattern.fullmatch(cod_new):
        tmp = list(collection)
        tmp[2] = cod_new
        # tuple(item for item in tmp)
        return (*tmp,)
    return None


def extract_data(src: SourceData):
    cut = src.df[src.df['H'].notna()].filter(['B', 'C', 'D', 'E', 'F', 'H'])

    column_name = src_model['заголовок']['column_name']
    re_collection_title = src_model['сборник']['title_pattern']
    print(f"Сборник: столбец заголовка {column_name!r}, шаблон для поиска: {re_collection_title!r}", )

    collections_quote = cut[cut[column_name].str.contains(re_collection_title, case=False, regex=True)]
    print(collections_quote)

    collections = [get_collection_data(row, collections_quote) for row in range(collections_quote.shape[0])]
    # print('Сборники:', len(collections))
    # pprint(collections, width=300)

    re_compiled_code = re.compile(src_model['сборник']['code_pattern'])
    print(f">> {'-' * 40}")
    bug_collections = {i: x for i, x in enumerate(collections) if re_compiled_code.fullmatch(x[2]) is None}
    pprint(bug_collections, width=300)
    print(f"{'-' * 40} <<")

    repaired = {}
    for key, value in bug_collections.items():
        print('------>>>> ', key, value)
        new = try_repair(value, re_compiled_code)
        if new:
            repaired[key] = new
    pprint(repaired, width=300)



    service_data['collections'].update({x[2]: x for x in collections})
    # pprint(service_data['collections'], width=300)

    del collections_quote
    gc.collect()
