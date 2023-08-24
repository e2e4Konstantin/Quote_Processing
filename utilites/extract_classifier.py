import pandas
from pandas import DataFrame
import gc
from pprint import pprint

from settings import service_data, console_colors, classifier, Node
from .get_duplicates import get_duplicates
from settings import SourceData


def get_abc_data(row: int, df: DataFrame) -> Node:
    """ Получает данные из строки row столбцов A, B, C. Возвращает экземпляр класса Node: """
    index = df.index[row]
    parent_code = str(df.at[index, 'A']).strip()
    code = df.at[index, 'B'].strip()
    field = df.at[index, 'C'].split()
    number = field[1][:-1]
    title = " ".join(field[2:])
    return Node(row=index, parent_code=parent_code, code=code, number=number, title=title)


def sheet_extract(file_name: str, file_path: str, sheet_name: str):
    """ Формирует словарь service_data[sheet_name]. Читает данные из листа sheet_name. """

    data = SourceData(file_name, file_path, sheet_name, skip_rows=1, data_from='file')
    data.df[data.df.columns] = data.df[data.df.columns].astype(pandas.pandas.StringDtype())
    # print(data.df.info())
    # print(data.df.head())
    item_counter = data.df[(data.df['B'].notna()) & (data.df['B'].str.strip() != '')].filter('B').count()
    print(f"в столбце 'B' прочитано строк: {item_counter.values[0]}")

    items = [get_abc_data(row, data.df) for row in range(data.df.shape[0])]
    service_data[sheet_name].update({item.code: item for item in items})

    if len(service_data[sheet_name]) != len(items):
        duplicates = get_duplicates([item.code for item in items])
        error_out = f"дубликаты: {console_colors['RED']}{duplicates}{console_colors['RESET']}"
        print(error_out)
    del data
    gc.collect()


def extract_classifier(file_path: str):
    file_name = r"classification.xlsx"
    # classifier = ['collections', 'sections', 'subsections', 'tables']
    for sheet_name in classifier:
        sheet_extract(file_name, file_path, sheet_name)


if __name__ == '__main__':
    extract_classifier(r"..\out")
