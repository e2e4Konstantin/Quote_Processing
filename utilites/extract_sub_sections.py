from pandas import DataFrame
import gc
import re
from re import Pattern
from pprint import pprint
from settings import src_model, service_data, console_colors, SubSection
from .get_duplicates import get_duplicates


def get_subsection_from_df(row: int, df: DataFrame) -> SubSection:
    """ Получает данные об Разделе из df на строке row. Возвращает экземпляр класса SubSection. """
    index = df.index[row]
    chapter_code = str(df.at[index, src_model['глава']['column_name']]).strip()
    collection_code = str(df.at[index, src_model['сборник']['column_name']]).strip()
    section_code = str(df.at[index, src_model['отдел']['column_name']]).strip()
    code = str(df.at[index, src_model['раздел']['column_name']]).strip()
    field = str(df.at[index, src_model['заголовок']['column_name']]).split()
    number = field[1][:-1]
    title = " ".join(field[2:])
    return SubSection(index, chapter_code, collection_code, section_code, code, number, title)


def subsections_extract(df: DataFrame):
    """ Извлекает Разделы из df и формирует словарь Разделов в общем хранилище service_data['subsections'].
        df -  без пустых значений в столбце 'H', столбцы ['B', 'C', 'D', 'E', 'F', 'H'] pandas dataframe.
    """
    column_name = src_model['заголовок']['column_name']
    re_subsection_title = src_model['раздел']['title_pattern']
    print(f"Раздел: столбец заголовка {column_name!r}, шаблон для поиска: {re_subsection_title!r}", )

    subsections_df = df[df[column_name].str.contains(re_subsection_title, case=False, regex=True)]
    subsections = [get_subsection_from_df(row, subsections_df) for row in range(subsections_df.shape[0])]
    print('Разделы:', len(subsections))


    re_code = re.compile(src_model['раздел']['code_pattern'])
    bug_subsections = {i: subsection.code for i, subsection in enumerate(subsections) if re_code.fullmatch(subsection.code) is None}
    if len(bug_subsections) > 0:
        print(f"'Разделы' с кривыми шифрами: {console_colors['YELLOW']}{bug_subsections}{console_colors['RESET']}")
        deleted = [subsections.pop(bs) for bs in bug_subsections]
        print(f"удалили {console_colors['YELLOW']}{len(deleted)}{console_colors['RESET']} Разделов с кривыми шифрами.")

    print('Разделы: ', subsections)
    # print(f"{'-' * 40}")
    # проверяем наличие Отдела у каждого Раздела
    # print('')
    # print('Отделы: ', service_data['sections'])
    if len(service_data['sections']) > 0:
        x0 = [subsection.section_code for i, subsection in enumerate(subsections)]
        x1 = list(service_data['sections'].keys())
        print(x0)
        print(x1)

        for z in x0:
            if z not in x1:
                print(z, False)

        x = [subsection.code for i, subsection in enumerate(subsections) if not service_data['sections'].get(subsection.section_code, None)]
        print(len(x), f'<{"-"* 50}>\n', x, f'\n<{"-"* 50}>')

        none_section = {i: subsection
                        for i, subsection in enumerate(subsections)
                        if service_data['sections'].get(subsection.section_code, None) is None
                        }
        print(len(none_section), f'{"*"* 50}\n', none_section, f'\n{"*"* 50}')
        # if len(none_section) > 0:
        #     print(f"'Разделы' без 'Отделов': {console_colors['YELLOW']}{none_section}{console_colors['RESET']}")
        #     deleted = [subsections.pop(bc) for bc in none_section]
        #     print(f"удалили {console_colors['YELLOW']}{len(deleted)}{console_colors['RESET']} Разделы' без 'Отделов'.")
    else:
        print(f"список Отделов {console_colors['YELLOW']}пустой{console_colors['RESET']}")
    # сохраняем данные
    service_data['subsections'].update({subsection.code: subsection for subsection in subsections})

    if len(service_data['subsections']) != len(subsections):
        duplicates = get_duplicates([subsection.code for subsection in subsections])
        error_out = f"Есть дубликаты 'Разделов': {console_colors['RED']}{duplicates}{console_colors['RESET']}"
        print(error_out)
    del subsections_df
    gc.collect()
