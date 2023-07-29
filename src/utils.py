from functools import lru_cache
from pathlib import Path

from fastapi import status
from fastapi.exceptions import HTTPException

from models.tile_operations import TileRequestParameters, TilePosition, TileAttributes, \
    GetTileRequest
from models.wmts_operations import WmtsRequestBase, RequestBase


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


async def get_request(
        layer: str,
        style: str,
        tilematrixset: str,
        service: str,
        request: str,
        version: str,
        format: str,
        tilematrix: str,
        tilecol: int,
        tilerow: int,
) -> RequestBase:
    """Возвращает класс по типу операции (request)."""
    # валидируем базовые операции
    try:
        WmtsRequestBase(
            service=service,
            request=request,
            version=version,)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) from e

    if request == 'gettile':
        return GetTileRequest(
            tilerequestparameters=TileRequestParameters(layer=layer, style=style),
            tileattributes=TileAttributes(
                format=format,
                tileposition=TilePosition(
                    tilematrixset=tilematrixset,
                    tilecol=tilecol,
                    tilerow=tilerow,
                    tilematrix=tilematrix
                )
            )
        )
    else:
        # TODO: заглушка для getCapabilities, getFeatureInfo
        pass
