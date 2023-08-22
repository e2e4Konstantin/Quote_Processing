from pandas import DataFrame
import gc
import re
from re import Pattern
from pprint import pprint
from settings import src_model, service_data, console_colors
from .get_duplicates import get_duplicates


def get_subsection_data_from_df(row: int, df: DataFrame) -> tuple[int, str, str, str, str, str, str]:
    """ Получает данные об Разделе из df на строке row.
            Возвращает кортеж:
                - номер строки в исходном файле. Он совпадает с индексом. 0
                - код главы. 1
                - код сборника. 2
                - код отдела. 3
                - код раздела. 4
                - номер раздела из названия. 5
                - название раздела. 6
        """
    index = df.index[row]
    chapter_cod = df.at[index, src_model['глава']['column_name']].strip()
    collection_cod = df.at[index, src_model['сборник']['column_name']].strip()
    section_cod = df.at[index, src_model['отдел']['column_name']].strip()
    subsection_cod = df.at[index, src_model['раздел']['column_name']].strip()
    subsection_field = df.at[index, src_model['заголовок']['column_name']].split()
    subsection_number = subsection_field[1][:-1]
    subsection_title = " ".join(subsection_field[2:])
    return index, chapter_cod, collection_cod, section_cod, subsection_cod, subsection_number, subsection_title


def repair_subsection(subsection: tuple[int, str, str, str, str, str, str], pattern: Pattern) -> tuple | None:
    """ Пытается починить строку Раздела, если у нее кривой код.
        Собирает новый код из кода Отдела + номер из названия Раздела.
        subsection - строка раздела.
        Возвращает отремонтированную строку Раздела либо None.
    """
    subsection_code_position = 4
    cod_new = f"{subsection[subsection_code_position-1]}-{subsection[subsection_code_position+1]}"
    if pattern.fullmatch(cod_new):
        tmp = list(subsection)
        tmp[subsection_code_position] = cod_new
        # tuple(item for item in tmp)
        return (*tmp,)
    return None


def subsections_extract(df: DataFrame):
    """ Извлекает Разделы из df и формирует словарь Разделов в общем хранилище service_data['subsections'].
        df -  без пустых значений в столбце 'H', столбцы ['B', 'C', 'D', 'E', 'F', 'H'] pandas dataframe.
    """
    column_name = src_model['заголовок']['column_name']
    re_subsection_title = src_model['раздел']['title_pattern']
    print(f"Раздел: столбец заголовка {column_name!r}, шаблон для поиска: {re_subsection_title!r}", )

    subsections_df = df[df[column_name].str.contains(re_subsection_title, case=False, regex=True)]
    subsections = [get_subsection_data_from_df(row, subsections_df) for row in range(subsections_df.shape[0])]
    print('Разделы:', len(subsections))
    # pprint(subsections, width=300)
    # print(f"{'-'*40}")

    re_code = re.compile(src_model['раздел']['code_pattern'])
    subsection_code_position = 4
    bug_subsections = {i: x for i, x in enumerate(subsections) if re_code.fullmatch(x[subsection_code_position]) is None}
    if len(bug_subsections) > 0:
        repaired = {key: rep_i for key, value in subsections_df.items() if (rep_i := repair_subsection(value, re_code))}
        print(f"отремонтированные Разделы: {repaired}")
        if len(repaired) > 0:
            for key in repaired.keys():
                subsections[key] = repaired[key]
                bug_subsections.pop(key, None)
        print(f"кривые 'Разделы': {console_colors['YELLOW']}{bug_subsections}{console_colors['RESET']}")

    service_data['subsections'].update({x[subsection_code_position]: x for x in subsections})

    if len(service_data['subsections']) != len(subsections):
        duplicates = get_duplicates([x[subsection_code_position] for x in subsections])
        error_out = f"Есть дубликаты 'Разделов': {console_colors['RED']}{duplicates}{console_colors['RESET']}"
        print(error_out)

    del subsections_df
    gc.collect()
