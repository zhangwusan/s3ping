from abc import ABC, abstractmethod
from typing import Any, Tuple, Optional, Dict
from requests.models import Response

from s3ping.core.utils.logger import Logger


class BaseMiddleware(ABC):
    def __init__(self):
        """
        Base class for all middleware with optional logger support.

        Args:
            logger (Optional[Any]): Logger instance (should support .debug, .info, .warning, .error).
        """

    @abstractmethod
    def process_request(self, url: str, kwargs: Dict[str, Any]) -> Any:
        """
        Hook to modify the request before it's made.

        Args:
            url (str): The request URL.
            kwargs (dict): Keyword arguments for the request (headers, proxies, etc.)

        Returns:
            Any:
                - Tuple[str, dict]: Modified URL and keyword arguments.
                - str (HTML content): If middleware chooses to bypass the HTTP call and handle request itself.
        """
        pass

    @abstractmethod
    def process_response(self, response: Optional[Response], **kwargs: Any) -> Optional[Response]:
        """
        Hook to process or modify the response after the request completes.

        Args:
            response (Response): The HTTP response object.
            kwargs: Additional arguments if needed.

        Returns:
            Response or None: Can return modified response or None to indicate failure or reprocessing needed.
        """
        pass