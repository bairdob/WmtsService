import traceback
import sqlite3

from fastapi import FastAPI, Request
from fastapi.responses import Response, JSONResponse

from database import AsyncSQLite
from models import MBTiles
from utils.utils import get_first_file_in_folder

app = FastAPI()


@app.exception_handler(Exception)
async def exception_handler(request, exc):
    error_response = {
        'message': str(exc),
        'traceback': traceback.format_exc(),
        'url': request.url._url,
    }
    return JSONResponse(status_code=500, content=error_response)


@app.get("/wmts", response_class=Response)
async def get_tile(layer: str,
                   style: str,
                   tilematrixset: str,
                   Service: str,
                   Request: str,
                   Version: str,
                   Format: str,
                   TileMatrix: int,
                   TileCol: int,
                   TileRow: int,
                   request: Request) -> Response:
    """Получаем тайл из БД."""

    if Service != 'WMTS' or Request != 'GetTile':
        return Response(
            content=f'Invalid request: {request.url._url}',
            status_code=400)

    if not layer.startswith('/'):
        layer = '/' + layer

    # инвертируем y
    TileRow = (1 << TileMatrix) - TileRow - 1

    # получаем путь к БД из параметра layer
    try:
        db_path = get_first_file_in_folder(layer, MBTiles.SUFFIX.value)
    except FileNotFoundError:
        return Response(
            content=f'File: {layer}*{MBTiles.SUFFIX.value} not found ',
            status_code=404)

    # получаем тайл из БД
    async with AsyncSQLite(db_path) as db:
        try:
            tile = await db.get_db_data(
                MBTiles.get_tile_query(z=TileMatrix, x=TileCol, y=TileRow))
        except sqlite3.OperationalError as e:
            return Response(
                content=f'Tile: {TileMatrix}, {TileCol}, {TileRow} not found ',
                status_code=404)

    return Response(content=tile[0], media_type='image/png')
