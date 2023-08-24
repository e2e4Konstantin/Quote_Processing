
from settings import SourceData
from .extract_data import extract_data


def parse_file_with_quotes(file_data: tuple[str, str, str], row_count=None, source_data='file') -> None:
    """ Получает исходные данные из файла и преобразовывает из в сервисную структуру.
        Входящий кортеж строк это: file_name, file_path, sheet_name
    """






    extract_data(data)
    # check_cod_quotes(data)
    # read_collection(data)
    # read_tables(data)
    # read_quotes(data)

