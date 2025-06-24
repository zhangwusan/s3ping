from abc import ABC, abstractmethod
from src.s3ping.loggers.logger import Logger
from src.s3ping.types.base import RequestType
from src.s3ping.responses.html import HTMLResponse


class BaseEngine(ABC):
    def __init__(self, logger=None):
        self.logger = logger or Logger(class_name=self.__class__.__name__)
        
    @abstractmethod
    def send(self, request: RequestType) -> HTMLResponse:
        """Send the request and return the response."""
        pass