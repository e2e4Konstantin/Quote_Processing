from pandas import DataFrame
from settings import service_data

def table_checking(table) -> bool:
    pass



def fill_tables_properties(df: DataFrame):
    """ Извлекает заголовки характеристик Таблиц из df.
    (статистику, атрибуты и параметры)
    df - исходный raw dataframe прочитанный из файла.
    """
    if len(service_data['tables']) > 0:
        for table in service_data['tables'].values():
            print(table)
            # if table_checking(table):
            #     get_table_properties(table, df)
