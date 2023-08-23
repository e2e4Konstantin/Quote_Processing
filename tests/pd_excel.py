import pandas
from pandas import DataFrame
import gc
import re

from pprint import pprint

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


f=r"F:\Kazak\GoogleDrive\1_KK\Job_CNAC\Python_projects\Quote_Processing\src\XXX_11.xlsx"

df = pandas.read_excel(io=f, sheet_name='name', header=None, dtype="object")
print(df)
print(df.info(verbose=False, show_counts=True))
names = generate_column_names(df.shape[1])
df.columns = names
# df.dropna()
print(df)
print(df.info(verbose=False, show_counts=True))
df = df.convert_dtypes()
print(df)
print(df.info(verbose=False, show_counts=True))

cd = df[df['H'].notna()].filter(['B', 'C', 'D', 'E', 'F', 'H'])
print(cd)
print(cd.info())
# cd['H'] = cd['H'].astype(pandas.StringDtype())

cd = cd[cd.columns].astype(pandas.StringDtype())

print(cd.info())
print(cd['H'])
print(cd['H'].str.contains(r"^\s*Отдел\s+\d+\.", case=False, regex=True))
sdf = cd[cd['H'].str.contains(r"^\s*Отдел\s+\d+\.", case=False, regex=True)]
print(sdf)