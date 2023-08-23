import sys
import pandas
from filetools import get_full_file_name
from settings.colors import console_colors
import pickle
import gc


def generate_column_names(length: int) -> list[str] | None:
    """ Создает список названий столбцов таблиц excel """
    alphabet = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    extra = []
    if 0 < length < 676:
        if length > len(alphabet):
            extra.extend(alphabet)
            for letter in alphabet:
                for letter_next in alphabet:
                    extra.append(f"{letter}{letter_next}")
                    if len(extra) >= length:
                        break
                if len(extra) >= length:
                    break
            return extra[:length]
        return alphabet[:length]
    return None


class SourceData:
    """ Класс для чтения данных в pandas data frame из указанной страницы excel файла.
        Читается Вся страница целиком.
        :parameter
        file_name: имя файла
        file_path: путь к файлу
        sheet_name: имя листа с которого читаем данные
    """

    def __init__(self, file_name: str = None, file_path: str = None, sheet_name: str = None,
                 skip_rows: int = None, row_count: int = None, data_from: str = 'file'):
        self.full_name = ""
        self.sheet_name = ""
        self.df: pandas.DataFrame() = None
        self.column_names = []
        self.row_max = 0
        self.column_max = 0
        self.get_data_from_excel(file_name, file_path, sheet_name, skip_rows, row_count, data_from)

    def get_data_from_excel(self, file_name: str = None, file_path: str = None, sheet_name: str = None,
                            skip_rows: int = 0, row_count: int = None, data_from: str = 'file'):
        """ Читает данные из файла.
            - именует столбцы как в excel таблице
            - удаляет пустые столбцы
            - преобразовывает типы данных столбцов к формату dtypes pandas
        """
        full_name = get_full_file_name(file_name, file_path)
        if full_name:
            try:
                self.df = pandas.read_excel(io=full_name, sheet_name=sheet_name, header=None, dtype="object",
                                            skiprows=skip_rows, nrows=row_count)
            except Exception as err:
                error_out = f"{console_colors['RED']}{err}{console_colors['RESET']}"
                show_full_name = f"'{console_colors['YELLOW']}{full_name}{console_colors['RESET']}'"
                print(f"ошибка при чтении данных из файла {show_full_name}:\n\t-->> {error_out}")
                sys.exit()
            if not self.df.empty:
                self.full_name = full_name
                self.sheet_name = sheet_name
                names = generate_column_names(self.df.shape[1])
                self.df.columns = names
                # self.df.dropna()
                self.df = self.df.convert_dtypes()
                self.row_max = self.df.shape[0] - 1
                self.column_max = self.df.shape[1] - 1
                self.column_names.extend(list(self.df.columns))
                print(f"данные успешно прочитаны из файла: {full_name},\nлист: '{sheet_name}'.")
                # self.df.to_pickle(f"{self.full_name[:-4]}pickle")
            else:
                raise TypeError(self.__class__)
        else:
            show_full_name = f"'{console_colors['YELLOW']}{full_name}{console_colors['RESET']}'"
            print(f"Не найден excel файл с данными {show_full_name}.")
            sys.exit()

    def __str__(self):
        return f"файл: {self.full_name}\nтаблица: {self.sheet_name}', строк: {self.row_max + 1}, столбцов: {self.column_max + 1}\n" \
               f"pandas.version: {pandas.__version__}"

    def get_cell_str_value(self, row, column) -> str:
        """ Возвращает значение ячейки из dataframe с адресом (row, column),
            преобразованное в строку, с удалением двойных пробелов."""
        if row >= 0 and column >= 0:
            src_value = self.df.iat[row, column]
            if pandas.isna(src_value):
                return ""
            match src_value:
                case int() | float():
                    return str(src_value)
                case str():
                    return " ".join(src_value.split())
                case _:
                    return str(src_value or "").strip()
        return ""

    def write_to_picle(self):
        with open(r'output\out_string.pickle', 'wb') as handle:
            pickle.dump(self.df, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def printing_dataset_information(self):
        print(f"{self.df.info(verbose=False, show_counts=True, memory_usage='deep')}")
        print(f"использовано памяти: {self.df.memory_usage(index=True, deep=True).sum():_} bytes")
        print(f"размерность: {self.df.shape}")
        print(f"индексы: {self.df.index}")
        print(f"названия столбцов: {self.df.columns.values.tolist()}")
        print(f"типы данных столбцов: {self.df.dtypes.values.tolist()}")
        # print(f"\n{self.df.head(3)}")


if __name__ == "__main__":
    path = r"F:\Kazak\GoogleDrive\1_KK\Job_CNAC\1_targets\tasck_2\sources"
    file = r"template_3_68.xlsx"
    sheet = r"name"
    data = SourceData(file, path, sheet, skip_rows=0, row_count=8300)
    print(data.printing_dataset_information())
    del data
    gc.collect()
