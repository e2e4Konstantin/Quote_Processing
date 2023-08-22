from pandas import DataFrame
import gc
import re
from re import Pattern
# from pprint import pprint

from settings import src_model, service_data, console_colors
from .get_duplicates import get_duplicates


def get_section_data_from_df(row: int, df: DataFrame) -> tuple[int, str, str, str, str, str]:
    """ Получает данные об Отделе из df на строке row.
            Возвращает кортеж:
                - номер строки в исходном файле. Он совпадает с индексом.
                - код главы
                - код сборника
                - код отдела
                - номер отдела из названия
                - название отдела
        """
    # код отдела формируется синтетически f"{section_cod}-{section_number}"
    # потому что в строке отдела он записан неправильно как код сборника
    index = df.index[row]
    chapter_cod = df.at[index, src_model['глава']['column_name']].strip()
    collection_cod = df.at[index, src_model['сборник']['column_name']].strip()
    section_cod = df.at[index, src_model['отдел']['column_name']].strip()
    section_field = df.at[index, src_model['заголовок']['column_name']].split()
    section_number = section_field[1][:-1]
    section_title = " ".join(section_field[2:])
    return index, chapter_cod, collection_cod, f"{section_cod}-{section_number}", section_number, section_title


def try_repair_section(section: tuple[int, str, str, str, str, str], pattern: Pattern) -> tuple | None:
    """ Пытается починить строку Отдела, если у нее кривой код.
        Собирает новый код из кода Сборника + номер из названия Отдела.
        section - строка отдела.
        Возвращает отремонтированную строку Отдела либо None.
    """
    section_code_position = 3
    cod_new = f"{section[section_code_position - 1]}-{section[section_code_position + 1]}"
    if pattern.fullmatch(cod_new):
        tmp = list(section)
        tmp[section_code_position] = cod_new
        # tuple(item for item in tmp)
        return (*tmp,)
    return None


def sections_extract(df: DataFrame):
    """ Извлекает Отделы из df и формирует словарь Отделов в общем хранилище service_data['sections'].
        df -  без пустых значений в столбце 'H', столбцы ['B', 'C', 'D', 'E', 'F', 'H'] pandas dataframe.
    """
    column_name = src_model['заголовок']['column_name']
    re_section_title = src_model['отдел']['title_pattern']
    print(f"Отдел: столбец заголовка {column_name!r}, шаблон для поиска: {re_section_title!r}", )

    sections_df = df[df[column_name].str.contains(re_section_title, case=False, regex=True)]
    sections = [get_section_data_from_df(row, sections_df) for row in range(sections_df.shape[0])]
    print('Отделы:', len(sections))
    # pprint(sections, width=300)
    # print(f"{'-'*40}")

    re_code = re.compile(src_model['отдел']['code_pattern'])
    section_code_position = 3
    bug_sections = {i: x for i, x in enumerate(sections) if re_code.fullmatch(x[section_code_position]) is None}
    if len(bug_sections) > 0:
        repaired = {key: rep_i for key, value in sections_df.items() if (rep_i := try_repair_section(value, re_code))}
        print(f"отремонтированные Отделы: {repaired}")
        if len(repaired) > 0:
            for key in repaired.keys():
                sections[key] = repaired[key]
                bug_sections.pop(key, None)
        print(f"кривые 'Отделы': {console_colors['YELLOW']}{bug_sections}{console_colors['RESET']}")
    service_data['sections'].update({x[section_code_position]: x for x in sections})

    if len(service_data['sections']) != len(sections):
        duplicates = get_duplicates([x[section_code_position] for x in sections])
        error_out = f"Есть дубликаты 'Отделов': {console_colors['RED']}{duplicates}{console_colors['RESET']}"
        print(error_out)

    del sections_df
    gc.collect()
