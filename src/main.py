import traceback

from fastapi import FastAPI
from fastapi.responses import Response, JSONResponse

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
                   TileRow: int):
    if not layer.startswith('/'):
        layer = '/' + layer
    data = {
        'layer': layer,
        'style': style,
        'tilematrixset': tilematrixset,
        'Service': Service,
        'Request': Request,
        'Version': Version,
        'Format': Format,
        'TileMatrix': TileMatrix,
        'TileCol': TileCol,
        'TileRow': TileRow,
        'file': get_first_file_in_folder(layer, '.mbtiles')
    }

    return JSONResponse(content=data)
