import sqlite3

from fastapi import status
from fastapi.exceptions import HTTPException

from database import AsyncSQLite
from models.mbtiles import MBTiles
from models.ogc_web_service import OGCWebService
from utils import get_first_file_in_folder


class WmtsService(OGCWebService):
    async def get_capabilities(self):
        pass

    @staticmethod
    async def get_tile(layer: str, tilematrix: int, tilerow: int, tilecol: int):
        """
        Возвращает тайл из базы данных.

        :param layer: слой (путь в файловой системе)
        :param tilematrix: Масштабный уровень
        :param tilerow: Координата X
        :param tilecol: Коодината Y
        :return: тайл
        """
        # инвертируем y
        tilerow = (1 << tilematrix) - tilerow - 1

        # получаем путь к БД из параметра layer
        try:
            db_path = get_first_file_in_folder(layer, MBTiles.SUFFIX.value)
        except FileNotFoundError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'File: {layer}*{MBTiles.SUFFIX.value} not found'
            ) from None

        # получаем тайл из БД
        async with AsyncSQLite(db_path) as db:
            try:
                tile = await db.get_db_data(
                    MBTiles.select_tile(z=tilematrix, x=tilecol, y=tilerow))
            except sqlite3.OperationalError as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Tile: {tilematrix}, {tilecol}, {tilerow} not found"
                ) from e

        return tile[0]

    async def get_feature_info(self):
        pass
