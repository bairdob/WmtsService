from functools import lru_cache
from pathlib import Path


@lru_cache(maxsize=64)
def get_first_file_in_folder(path: str, extension: str) -> str:
    """
    Возвращает полный путь к первому файлу в папке с заданным расширением.

    :param path: Путь к папке.
    :param extension: Расширение файла.
    :return: Полный путь к первому файлу по расширению.
    :raises FileNotFoundError: Если в папке не найден файл с указанным расширением.
    """
    path = Path(path)
    if path.is_file():
        return str(path)
    for file_path in path.iterdir():
        if file_path.is_file() and file_path.name.endswith(extension):
            return str(file_path)
    raise FileNotFoundError(f"В папке '{path}' не найден файл с расширением '{extension}'.")
