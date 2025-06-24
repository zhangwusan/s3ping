from typing import Optional
from src.s3ping.types.base import NextHandlerType, RequestType, ResponseType
from src.s3ping.logger.logger import Logger


class BaseMiddleware:

    def __init__(self, logger: Optional[Logger] = None):
        self.logger = logger or Logger(class_name=self.__class__.__name__)

    def process(self, request: RequestType, next: NextHandlerType) -> ResponseType:
        """
        Process the request and/or response.
        - request: Dictionary with keys like 'url', 'headers', etc.
        - next_handler: A callable that takes the request and returns a response.
        - returns: The final response after processing.
        """
        raise NotImplementedError("Subclasses must implement this method.")