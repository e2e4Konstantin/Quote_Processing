from dataclasses import dataclass, field, fields


@dataclass
class Collection:
    """ Сборник:
            - номер строки в исходном файле.
            - код главы
            - код сборника
            - номер сборника из названия
            - название
     """
    row: int
    chapter_code: str
    code: str
    number: str
    title: str

    def __str__(self):
        s = ', '.join(f'{getattr(self, x.name)!r}' for x in fields(self))
        return f"{type(self).__name__}({s})"

    def __repr__(self):
        s = ', '.join(f'{getattr(self, x.name)!r}' for x in fields(self))
        return f"({s})"

    def info(self):
        s = '; '.join(f'{x.name}={getattr(self, x.name)!r}' for x in fields(self))
        return f'{type(self).__name__}({s})'


@dataclass
class Section:
    """ Отдел
        - номер строки в исходном файле.
        - код главы
        - код сборника
        - код отдела
        - номер Отела из названия
        - название
    """
    row: int
    chapter_code: str
    collection_code: str
    code: str
    number: str
    title: str

    def __str__(self):
        s = ', '.join(f'{getattr(self, x.name)!r}' for x in fields(self))
        return f"{type(self).__name__}({s})"

    def __repr__(self):
        s = ', '.join(f'{getattr(self, x.name)!r}' for x in fields(self))
        return f"({s})"

    def info(self):
        s = '; '.join(f'{x.name}={getattr(self, x.name)!r}' for x in fields(self))
        return f'{type(self).__name__}({s})'


@dataclass
class SubSection:
    """ Раздел (номер строки; код главы; код сборника; код отдела;
        код Раздела; номер Раздела из названия; название) """
    row: int
    chapter_code: str
    collection_code: str
    section_code: str
    code: str
    number: str
    title: str

    def __str__(self):
        s = ', '.join(f'{getattr(self, x.name)!r}' for x in fields(self))
        return f"{type(self).__name__}({s})"

    def __repr__(self):
        s = ', '.join(f'{getattr(self, x.name)!r}' for x in fields(self))
        return f"({s})"

    def info(self):
        s = '; '.join(f'{x.name}={getattr(self, x.name)!r}' for x in fields(self))
        return f'{type(self).__name__}({s})'


@dataclass
class Header:
    """Заголовок универсальный """
    column_header: int = 0  # номер столбца заголовка
    name_header: str = ""  # название заголовка


@dataclass
class OptionHeader:
    """ Название параметра: заголовок таблицы параметра """
    column_option_header: int = 0  # первая колонка заголовка параметров
    name_option_header: str = ""  # название таблицы параметров
    option_headers: list[Header] = field(default_factory=list)  # список заголовков значений параметра


@dataclass
class Table:
    """ Таблица """
    row: int  # номер строки начала таблицы
    cod: str  # код таблицы
    number: str  # номер/печатный из названия
    name: str  # название
    section: SubSection  # указатель на отдел

    # catalog_table: list[str] = field(default_factory=list)  # ссылки на каталог
    attributes: list[Header] = field(default_factory=list)  # список заголовков атрибутов
    options: list[OptionHeader] = field(default_factory=list)  # список заголовков параметров

    def __str__(self):
        return f"row:{self.row:4}, {self.cod}, {self.number:8}, {self.name}, " \
               f"атрибутов: {len(self.attributes)}, параметров: {len(self.options)},   " \
               f"{self.attributes}, {self.options}"

    def table_to_list(self) -> list:
        # catalog = ', '.join(x for x in self.catalog_table)
        attributes = ', '.join(x.name_header for x in self.attributes)
        option = ', '.join(x.name_header_option for x in self.options)
        return [self.row, self.cod, self.number, self.name, len(self.attributes), len(self.options), attributes, option]


# --------------------------------------------------------------------------------------------------

""" сервисные данные добытые из файла"""

dict_collections: dict[str: Collection] = {}
dict_sections: dict[str: Section] = {}
dict_sub_sections: dict[str: SubSection] = {}
dict_tables: dict[str: Table] = {}

service_data = {
    "collections": dict_collections,
    "sections": dict_sections,
    "subsections": dict_sub_sections,
    "tables": dict_tables

}

if __name__ == '__main__':
    data_1 = (18179, '3', '3.51', '51', 'Прочие строительные работы')
    data_2 = (16615, '3', '3.39', '39', 'Металлические конструкции гидротехнических сооружений')
    c = Collection(*data_1)
    service_data["collections"]['895**'] = Collection(*data_2)

    print(c)
    print(service_data)
