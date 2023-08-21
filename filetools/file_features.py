import os


def check_full_file_name(file_name: str, file_path: str = "") -> str | None:
    """ Создает абсолютный путь к файлу. Возвращает путь если файл существует """
    if file_name:
        test_path = os.path.abspath(os.path.join(file_path, file_name))
        if os.path.exists(test_path):
            return test_path
    return None


def get_full_file_name(file_name: str, file_path: str = "") -> str | None:
    """ Создает абсолютный путь к файлу. """
    if file_name:
        return os.path.abspath(os.path.join("" if file_path is None else file_path, file_name))
    return None


def does_file_in_use(abs_file_name: str) -> bool:
    """ Проверяет, занят или нет указанный по абсолютному маршруту файл """
    if abs_file_name and os.path.exists(abs_file_name):
        try:
            os.rename(abs_file_name, abs_file_name)
            return False
        except IOError:
            return True
    return False


if __name__ == "__main__":
    fln = "file_features.py"
    print(f"{os.getcwd() = }")
    print(f"{os.path.dirname(fln) = }")
    print(f"{os.path.exists(fln) = }")
    print(f"файл '{fln}' занят: {does_file_in_use(fln)}")
    print(f"файл '' занят: {does_file_in_use('')}")
