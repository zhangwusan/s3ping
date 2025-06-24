from abc import ABC, abstractmethod
from src.s3ping.types.base import RequestType
from src.s3ping.responses.html import HTMLResponse


class BaseEngine(ABC):
    @abstractmethod
    def send(self, request: RequestType) -> HTMLResponse:
        """Send the request and return the response."""
        pass