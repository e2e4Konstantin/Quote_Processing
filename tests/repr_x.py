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
        s = '; '.join(f'{x.name}={getattr(self, x.name)!r}' for x in fields(self))
        return f'{type(self).__name__}({s})'

    def __repr__(self):
        s = ', '.join(f'{getattr(self, x.name)!r}' for x in fields(self))
        return f"{type(self).__name__}({s})"

m1 = Collection(18194, '3', '3.51', '51', 'Технический надзор за строительством тепловых сетей')
print(m1)
print(repr(m1))
# mydate2 = eval(repr(mydate1))
