import pandas
import gc
from settings import SourceData, service_data, classifier, src_model, tables_stock, Table, console_colors
from .extract_classifier import extract_classifier
from utilites.get_duplicates import get_duplicates


def extract_data(file_data: tuple[str, str, str], row_count=None):
    file_name, file_path, sheet_name = file_data

    # заполнить классификатор service_data из файла classification.xlsx
    extract_classifier(file_path)
    # for x in service_data.keys():
    #     print(f"{x}: {service_data[x]}")
    print(f"Прочитано в service_data: ")
    print(f"\tСборники: {len(service_data[classifier[0]])}")
    print(f"\tОтделы: {len(service_data[classifier[1]])}")
    print(f"\tРазделы: {len(service_data[classifier[2]])}")
    print(f"\tТаблицы: {len(service_data[classifier[3]])}")

    data = SourceData(file_name, file_path, sheet_name)     # , skip_rows=4
    data.printing_dataset_information()
    # print(data.df.head(10))
    c = data.df[(data.df['F'].notna()) & (data.df['G'].str.strip() != '')].filter('G').count()
    print(f"непустых значений в столбце 'G': {c.values[0]}")

    useful_columns = ['F', 'H']
    df = data.df[data.df['F'].notna()].filter(useful_columns)
    df[df.columns] = df[df.columns].astype(pandas.pandas.StringDtype())
    target_column = src_model['заголовок']['column_name']
    re_table_title = src_model['таблица']['title_pattern']
    print(f"Таблица: столбец заголовка {target_column!r}, шаблон для поиска: {re_table_title!r}", )
    df = df[df['H'].str.contains(re_table_title, case=False, regex=True)]
    print(df.info())
    print(df.head(5))
    # print(service_data['tables'])

    tables_in_file = [df.at[df.index[row], 'F'].strip() for row in range(df.shape[0])]
    for row in range(df.shape[0]):
        index = df.index[row]
        tables_code = df.at[index, 'F'].strip()
        node_table = service_data['tables'].get(tables_code, None)
        if node_table:
            tables_stock[tables_code] = Table(row=index)
        else:
            print(f"таблицы с кодом {tables_code} в классификаторе не найдено.")
    print(f"сохранено таблиц: {len(tables_stock)}, таблиц в файле: {len(tables_in_file)}")
    if len(tables_stock) != len(tables_in_file):
        duplicates = get_duplicates(tables_in_file)
        error_out = f"Есть дубликаты 'Таблиц': {console_colors['RED']}{duplicates}{console_colors['RESET']}"
        print(error_out)


    #
    # # columns = ['B', 'C', 'D', 'E', 'F', 'H']
    # # cut = src.df[src.df['H'].notna()].filter(columns)
    # # cut = cut[cut.columns].astype(pandas.StringDtype())
    # # print(cut.info())
    # # del cut
    # # gc.collect()
    #
    # del data
    # gc.collect()
