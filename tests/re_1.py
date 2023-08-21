import re
from re import Pattern

src = {
    '1936-03-01 00:00:00': (16460, '3', '1936-03-01 00:00:00', '36', 'Земляные конструкции гидротехнических сооружений'),
    '3.0': (4, '3', '3.0', '0', 'Общие положения'),
    '3.1': (7, '3', '3.1', '1', 'Земляные работы'),
    '3.10': (4826, '3', '3.10', '10', 'Деревянные конструкции'),
    '3.11': (5531, '3', '3.11', '11', 'Полы'),
    '3.12': (5791, '3', '3.12', '12', 'Кровли'),
    '3.13': (6024, '3', '3.13', '13', 'Защита строительных конструкций и оборудования от коррозии'),
    '3.14': (6324, '3', '3.14', '14', 'Конструкции в сельском строительстве'),
    '3.15': (6357, '3', '3.15', '15', 'Отделочные работы'),
    '3.16': (7769, '3', '3.16', '16', 'Трубопроводы внутренние'),
    '3.17': (8123, '3', '3.17', '17', 'Водопровод и канализация - внутренние устройства'),
    '3.18': (8210, '3', '3.18', '18', 'Отопление - внутренние устройства'),
    '3.19': (8414, '3', '3.19', '19', 'Газоснабжение - внутренние устройства'),
    '3.20': (8507, '3', '3.20', '20', 'Вентиляция и кондиционирование воздуха'),
    '3.22': (9079, '3', '3.22', '22', 'Водопровод - наружные сети'),
    '3.23': (9806, '3', '3.23', '23', 'Канализация - наружные сети'),
    '3.24': (10233, '3', '3.24', '24', 'Теплоснабжение и газопроводы - наружные сети'),
    '3.26': (10933, '3', '3.26', '26', 'Теплоизоляционные работы'),
    '3.27': (11211, '3', '3.27', '27', 'Автомобильные дороги'),
    '3.28': (11750, '3', '3.28', '28', 'Железные дороги'),
    '3.29': (12400, '3', '3.29', '29', 'Тоннели и метрополитены'),
    '3.3': (555, '3', '3.3', '3', 'Буровзрывные работы'),
    '3.30': (15011, '3', '3.30', '30', 'Мосты и трубы'),
    '3.32': (15551, '3', '3.32', '32', 'Трамвайные пути'),
    '3.33': (15739, '3', '3.33', '33', 'Линии электропередачи'),
    '3.34': (16083, '3', '3.34', '34', 'Сооружения связи, радиовещания и телевидения'),
    '3.37': (16476, '3', '3.37', '37', 'Бетонные и железобетонные конструкции гидротехнических сооружений'),
    '3.38': (16598, '3', '3.38', '38', 'Каменные конструкции гидротехнических сооружений'),
    '3.39': (16615, '3', '3.39', '39', 'Металлические конструкции гидротехнических сооружений'),
    '3.4': (834, '3', '3.4', '4', 'Скважины'),
    '3.40': (16640, '3', '3.40', '40', 'Деревянные конструкции гидротехнических сооружений'),
    '3.41': (16703, '3', '3.41', '41', 'Гидроизоляционные работы в гидротехнических сооружениях'),
    '3.42': (16751, '3', '3.42', '42', 'Берегоукрепительные работы'),
    '3.44': (16853, '3', '3.44', '44', 'Подводно-строительные (водолазные) работы'),
    '3.45': (17250, '3', '3.45', '45', 'Промышленные печи и трубы'),
    '3.47': (17588, '3', '3.47', '47', 'Озеленение, благоустройство, малые формы'),
    '3.5': (1349, '3', '3.5', '5', 'Свайные работы, закрепление грунтов'),
    '3.51': (18179, '3', '3.51', '51', 'Прочие строительные работы'),
    '3.6': (2259, '3', '3.6', '6', 'Бетонные, железобетонные конструкции монолитные'),
    '3.7': (3043, '3', '3.7', '7', 'Бетонные, железобетонные конструкции сборные'),
    '3.8': (4083, '3', '3.8', '8', 'Конструкции из кирпича и блоков'),
    '3.9': (4394, '3', '3.9', '9', 'Металлические конструкции')}
src_keys = list(src.keys())
print(src_keys)
cp = re.compile(r"^\s*\d+\.\d+\s*$")
print(type(cp))

v = src_keys[0]
r = cp.findall(v)
print(r)

r1 = cp.fullmatch(src_keys[0], )
print(r1)

# for i, v in enumerate(src):
#     print(i, v)

s = {31: (16460, '3', '1936-03-01 00:00:00', '36', 'Земляные конструкции гидротехнических сооружений')}
print(type(s), s)
print(s.keys())
print(s.values())


for i, (k, v) in enumerate(s.items()):
    print(i, k, v)