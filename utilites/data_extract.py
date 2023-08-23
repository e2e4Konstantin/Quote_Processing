import pandas
import gc
from settings import SourceData, service_data

import itertools

from pprint import pprint

from .extract_collections import collections_extract
from .extract_sections import sections_extract
from .extract_sub_sections import subsections_extract
from .extract_tables import tables_extract
from .fill_tables_properties import fill_tables_properties


def extract_data(src: SourceData):
    columns = ['B', 'C', 'D', 'E', 'F', 'H']
    cut = src.df[src.df['H'].notna()].filter(columns)
    cut = cut[cut.columns].astype(pandas.StringDtype())
    print(cut.info())

    collections_extract(cut)
    sections_extract(cut)
    subsections_extract(cut)
    # tables_extract(cut)

    # pprint(service_data['collections'], width=300)
    print("результат 'sections': ",)
    pprint( service_data['sections'], width=300)
    # pprint(service_data['subsections'], width=300)

    # pprint(dict(itertools.islice(service_data['tables'].items(), 10)), width=300)
    print(f"Прочитано: ")
    print(f"\tСборники: {len(service_data['collections'])}")
    print(f"\tОтделы: {len(service_data['sections'])}")
    print(f"Разделы: {len(service_data['subsections'])}")
    # print(f"Таблицы: {len(service_data['tables'])}")

    # fill_tables_properties(src)


    del cut
    gc.collect()
