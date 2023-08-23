import gc
from settings import SourceData
from .data_extract import extract_data


def parse_file_with_quotes(file_data: tuple[str, str, str], row_count=None, source_data='file') -> None:
    """ Получает исходные данные из файла и преобразовывает из в сервисную структуру.
        Входящий кортеж строк это: file_name, file_path, sheet_name
    """
    file_name, file_path, sheet_name = file_data
    data = SourceData(file_name, file_path, sheet_name, row_count=row_count, data_from=source_data)
    data.printing_dataset_information()



    c = data.df[(data.df['G'].notna()) & (data.df['G'].str.strip() != '')].filter('G').count()
    print(f"непустых значений в столбце 'G': {c.values[0]}")

    extract_data(data)
    # check_cod_quotes(data)
    # read_collection(data)
    # read_tables(data)
    # read_quotes(data)
    del data
    gc.collect()
