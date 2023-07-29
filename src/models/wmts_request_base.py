from abc import ABC

from pydantic import BaseModel, field_validator


class RequestBase(ABC):
    pass


class WmtsRequestBase(BaseModel, RequestBase):
    """Сервисный класс WMTS. Содержит обязательные параметры запроса"""
    service: str  # сервис wmts
    request: str  # операция
    version: str  # версия стандарта wmts

    @field_validator('service')
    @classmethod
    def service_shall_wmts(cls, value: str) -> str:
        if value != 'wmts':
            raise ValueError('OperationNotSupported')
        return value

    @field_validator('request')
    @classmethod
    def request_shall_validator(cls, value: str) -> str:
        if value not in ('gettile', 'getcapabilities', 'getfeatureinfo'):
            raise ValueError('OperationNotSupported')
        return value

    @field_validator('version')
    @classmethod
    def version_shall_one(cls, value: str) -> str:
        if value != '1.0.0':
            raise ValueError('VersionNegotiationFailed')
        return value
