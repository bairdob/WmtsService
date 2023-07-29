from enum import Enum


class MBTiles(Enum):
    """Сервисный класс MBtiles."""
    DEFAULT_TABLE_NAME = 'tiles'
    TILE_COLUMN = 'tile_data'
    Z_COLUMN = 'zoom_level'
    X_COLUMN = 'tile_column'
    Y_COLUMN = 'tile_row'
    SUFFIX = '.mbtiles'

    @staticmethod
    def select_tile(z: int, x: int, y: int):
        """
        Возвращает SQL запрос для получения тайла.

        :param z: Масштабный уровень
        :param x: Координата Х
        :param y: Координата Y
        :return: SQL запрос
        """
        return f'''SELECT {MBTiles.TILE_COLUMN.value} FROM "{MBTiles.DEFAULT_TABLE_NAME.value}"
                       WHERE {MBTiles.Z_COLUMN.value}={z}
                            AND {MBTiles.X_COLUMN.value}={x}
                            AND {MBTiles.Y_COLUMN.value}={y}
                       LIMIT 1'''
