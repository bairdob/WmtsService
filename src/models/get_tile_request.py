from pydantic import BaseModel, field_validator

from models.wmts_request_base import RequestBase


class TileRequestParameters(BaseModel):
    layer: str  # слой (путь в файловой системе)
    style: str  # стиль

    @field_validator('layer')
    @classmethod
    def validate_layer_path(cls, value: str) -> str:
        if not value.startswith('/'):
            value = '/' + value
        return value


class TilePosition(BaseModel):
    tilematrixset: str  # система координат
    tilecol: int  # координата X
    tilerow: int  # координата Y
    tilematrix: str  # координата Z (масштабный уровень)


class TileAttributes(BaseModel):
    format: str  # маймтайп
    tileposition: TilePosition  # позиция тайла


class GetTileRequest(BaseModel, RequestBase):
    tilerequestparameters: TileRequestParameters
    tileattributes: TileAttributes
