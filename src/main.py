import hashlib
import sqlite3
import traceback

from fastapi import FastAPI, Request, status
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, JSONResponse

from database import AsyncSQLite
from models import MBTiles
from utils import get_first_file_in_folder

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DECODE_FORMAT = "latin-1"


@app.middleware("http")
async def case_sens_middleware(request: Request, call_next):
    """Мидлварь запросы не зависят от регистра."""
    raw_query_str = request.scope["query_string"].decode(DECODE_FORMAT).lower()
    request.scope["query_string"] = raw_query_str.encode(DECODE_FORMAT)

    path = request.scope["path"].lower()
    request.scope["path"] = path

    response = await call_next(request)
    return response


@app.exception_handler(Exception)
async def exception_handler(request, exc):
    error_response = {
        'message': str(exc),
        'traceback': traceback.format_exc(),
        'url': request.url._url,
    }
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response
    )


@app.get("/wmts", response_class=Response)
async def get_tile(layer: str,
                   style: str,
                   tilematrixset: str,
                   service: str,
                   request: str,
                   version: str,
                   format: str,
                   tilematrix: int,
                   tilecol: int,
                   tilerow: int,
                   _request: Request) -> Response:
    """Получаем тайл из БД."""

    if service != 'wmts' or request != 'gettile':
        return Response(
            content=f'Invalid request: {_request.url._url}',
            status_code=status.HTTP_400_BAD_REQUEST)

    if not layer.startswith('/'):
        layer = '/' + layer

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
                MBTiles.get_tile_query(z=tilematrix, x=tilecol, y=tilerow))
        except sqlite3.OperationalError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tile: {tilematrix}, {tilecol}, {tilerow} not found"
            ) from e

    return Response(
        content=tile[0],
        media_type='image/png',
        headers={
            'ETag': str(hashlib.sha256(tile[0]).hexdigest()),
            "Cache-Control": "max-age=604800"
        }
    )
