from pandas import DataFrame
import gc
import re

from pprint import pprint

from settings import src_model, service_data, console_colors, Section
from .get_duplicates import get_duplicates


def get_section_from_df(row: int, df: DataFrame) -> Section:
    """ Получает данные об Отделе из df на строке row.
        Возвращает экземпляр класса Section. """
    # код отдела формируется синтетически f"{section_cod}-{section_number}"
    # потому что в строке отдела он записан неправильно: как код сборника
    index = df.index[row]
    chapter_code = str(df.at[index, src_model['глава']['column_name']]).strip()
    collection_code = str(df.at[index, src_model['сборник']['column_name']]).strip()
    code = str(df.at[index, src_model['отдел']['column_name']]).strip()
    field = str(df.at[index, src_model['заголовок']['column_name']]).split()
    number = field[1][:-1]
    title = " ".join(field[2:])
    # print((index, chapter_code, collection_code, code, number, title))
    return Section(row=index, chapter_code=chapter_code, collection_code=collection_code, code=f"{code}-{number}",
                   number=number, title=title)


def sections_extract(df: DataFrame):
    """ Извлекает Отделы из df и формирует словарь Отделов в общем хранилище service_data['sections'].
        df -  без пустых значений в столбце 'H', столбцы ['B', 'C', 'D', 'E', 'F', 'H'] pandas dataframe.
    """
    column_name = src_model['заголовок']['column_name']
    re_section_title = src_model['отдел']['title_pattern']
    print(f"Отдел: столбец заголовка {column_name!r}, шаблон для поиска: {re_section_title!r}", )

    sections_df = df[df[column_name].str.contains(re_section_title, case=False, regex=True)]
    sections = [get_section_from_df(row, sections_df) for row in range(sections_df.shape[0])]
    print('Отделы:', len(sections))
    # pprint(sections, width=300)
    # print(f"{'-'*40}")

    re_code = re.compile(src_model['отдел']['code_pattern'])
    bug_sections = {i: section.code for i, section in enumerate(sections) if re_code.fullmatch(section.code) is None}
    if len(bug_sections) > 0:
        print(f"'Отделы' с кривыми шифрами: {console_colors['YELLOW']}{bug_sections}{console_colors['RESET']}")
        deleted = [sections.pop(bs) for bs in bug_sections]
        print(f"удалили {console_colors['YELLOW']}{len(deleted)}{console_colors['RESET']} Отделов с кривыми шифрами.")

    # проверяем наличие Сборника у каждого Отдела
    if len(service_data['collections']) > 0:
        none_collection_sections = {i: section
                                    for i, section in enumerate(sections)
                                    if service_data['collections'].get(section.collection_code, None) is None
                                    }
        if len(none_collection_sections) > 0:
            print(
                f"'Отделы' без Сборников: {console_colors['YELLOW']}{none_collection_sections}{console_colors['RESET']}")
            deleted = [sections.pop(bc) for bc in none_collection_sections]
            print(f"удалили {console_colors['YELLOW']}{len(deleted)}{console_colors['RESET']} Отделов без Сборника.")
    else:
        print(f"список Сборников {console_colors['YELLOW']}пустой{console_colors['RESET']}")
    # сохраняем данные
    service_data['sections'].update({section.code: section for section in sections})

    if len(service_data['sections']) != len(sections):
        duplicates = get_duplicates([section.code for section in sections])
        error_out = f"Есть дубликаты 'Отделов': {console_colors['RED']}{duplicates}{console_colors['RESET']}"
        print(error_out)

    del sections_df
    gc.collect()
