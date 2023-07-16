from fastapi import FastAPI
from fastapi.responses import JSONResponse


app = FastAPI()


@app.get("/wmts")
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
        'TileRow': TileRow
    }

    return JSONResponse(content=data)
