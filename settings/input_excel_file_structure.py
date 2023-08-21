model_data = [
    ('глава', 'B', r"^\s*\d+\s*$", r"^\s*Глава\s+\d+\."),
    ('сборник', 'C', r"^\s*\d+\.\d+\s*$", r"^\s*Сборник\s+\d+\."),
    ('отдел', 'D', r"^\s*\d+\.\d+(-\d+){1}\s*$", r"^\s*Отдел\s+\d+\."),
    ('раздел', 'E', r"^\s*\d+\.\d+(-\d+){2}\s*$", r"^\s*Раздел\s+\d+\."),
    ('таблица', 'F', r"^\s*\d+\.\d+(-\d+){4}\s*$", r"^\s*Таблица\s+\d+\.\d+-\d+\."),
    ('расценка', 'G', r"^\s*\d+\.\d+(-\d+){2}\s*$", r"."),
    ('заголовок', 'H', r".", r"."),
]


def create_dict(input_data: tuple[str, str, str]) -> dict[str: str]:
    column_name, re_column_pattern, re_title_pattern = input_data
    return {
        'column_name': column_name,
        'code_pattern': re_column_pattern,
        'title_pattern': re_title_pattern,
    }


src_model = {item[0]: create_dict(item[1:]) for item in model_data}

if __name__ == '__main__':
    from pprint import pprint

    pprint(src_model)
