from abc import ABC, abstractmethod

from pydantic import BaseModel


class OGCWebService(BaseModel, ABC):
    @abstractmethod
    def get_capabilities(self):
        pass

    class Config:
        arbitrary_types_allowed = True
        allow_abstract = True
