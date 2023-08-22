from pandas import DataFrame
import gc
import re
from re import Pattern
from pprint import pprint
from settings import src_model, service_data, console_colors
from .get_duplicates import get_duplicates


def get_table_from_df(row: int, df: DataFrame) -> tuple[int, str, str, str, str, str, str, str]:
    """ Получает данные о Таблице из df на строке row.
        Возвращает кортеж:
            - номер строки в исходном файле. Он совпадает с индексом. 0
            - код главы. 1
            - код сборника. 2
            - код отдела. 3
            - код раздела. 4
            - код таблицы 5
            - номер таблицы из названия. 6
            - название таблицы. 7
        """
    index = df.index[row]
    chapter_cod = df.at[index, src_model['глава']['column_name']].strip()
    collection_cod = df.at[index, src_model['сборник']['column_name']].strip()
    section_cod = df.at[index, src_model['отдел']['column_name']].strip()
    subsection_cod = df.at[index, src_model['раздел']['column_name']].strip()
    table_cod = df.at[index, src_model['таблица']['column_name']].strip()

    table_field = df.at[index, src_model['заголовок']['column_name']].split()
    table_number = table_field[1][:-1]
    table_title = " ".join(table_field[2:])
    return index, chapter_cod, collection_cod, section_cod, subsection_cod, table_cod, table_number, table_title


def tables_extract(df: DataFrame):
    """ Извлекает Таблицы из df и формирует словарь Таблиц в общем хранилище service_data['tables'].
        df -  без пустых значений в столбце 'H', столбцы ['B', 'C', 'D', 'E', 'F', 'H'] pandas dataframe.
    """
    column_name = src_model['заголовок']['column_name']
    re_table_title = src_model['таблица']['title_pattern']
    print(f"Таблица: столбец заголовка {column_name!r}, шаблон для поиска: {re_table_title!r}", )

    tables_df = df[df[column_name].str.contains(re_table_title, case=False, regex=True)]
    tables = [get_table_from_df(row, tables_df) for row in range(tables_df.shape[0])]
    print('Таблицы:', len(tables))
    # pprint(subsections, width=300)
    # print(f"{'-'*40}")

    re_code = re.compile(src_model['таблица']['code_pattern'])
    table_code_position = 5
    bug_tables = {i: x for i, x in enumerate(tables) if re_code.fullmatch(x[table_code_position]) is None}
    if len(bug_tables) > 0:
        print(f"кривые 'Таблицы': {len(bug_tables)}\n{console_colors['YELLOW']}{bug_tables}{console_colors['RESET']}")
        # удалить кривые таблицы из списка
        for key in bug_tables.keys():
            try:
                tables.pop(key)
            except IndexError as err:
                print(f"{console_colors['YELLOW']}ошибка при удалении таблицы из списка:{console_colors['RESET']}\n{err}")

    service_data['tables'].update({x[table_code_position]: x for x in tables})

    if len(service_data['tables']) != len(tables):
        duplicates = get_duplicates([x[table_code_position] for x in tables])
        if len(duplicates) > 0:
            error_out = f"Есть дубликаты 'Таблиц': {console_colors['RED']}{duplicates}{console_colors['RESET']}"
            print(error_out)
    del tables_df
    gc.collect()


