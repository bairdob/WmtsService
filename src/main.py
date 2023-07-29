import hashlib
import traceback

from fastapi import FastAPI, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, JSONResponse

from middleware import LowerCaseMiddleware
from models.get_tile_request import GetTileRequest
from models.wmts_request_base import RequestBase
from models.wmts_service import WmtsService
from utils import get_request

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.middleware("http")(LowerCaseMiddleware())


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


@app.get("/ping")
def ping():
    return {"message": "pong"}


@app.get("/wmts", response_class=Response)
async def get_resource(request: RequestBase = Depends(get_request)) -> Response:
    """Получаем тайл из БД."""
    if isinstance(request, GetTileRequest):
        tile = await WmtsService.get_tile(
            layer=request.tilerequestparameters.layer,
            tilematrix=int(request.tileattributes.tileposition.tilematrix),
            tilerow=request.tileattributes.tileposition.tilerow,
            tilecol=request.tileattributes.tileposition.tilecol
        )

        return Response(
            content=tile,
            media_type=request.tileattributes.format,
            headers={
                'ETag': str(hashlib.sha256(tile).hexdigest()),
                "Cache-Control": "max-age=604800"
            }
        )
