from typing import Any, Dict, Optional, Tuple
from fake_useragent import UserAgent
from requests.models import Response

from s3ping.core.utils.logger import Logger
from s3ping.middlewares.base import BaseMiddleware


class HeaderMiddleware(BaseMiddleware):
    def __init__(self, randomize: bool = False, logger: Logger = None):
        super().__init__()
        self.logger = Logger(class_name=self.__class__.__name__)

        self.randomize = randomize
        self.ua = UserAgent()

        self.logger.info(f"initialized | Randomize UA: {self.randomize}")

    def process_request(self, url: str, kwargs: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
        headers: Dict[str, str] = kwargs.get("headers", {})
        user_agent = self.ua.random if self.randomize else self.ua.chrome

        headers["User-Agent"] = user_agent
        headers.setdefault("Accept-Language", "en-US,en;q=0.9")
        headers.setdefault("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")
        headers.setdefault("Connection", "keep-alive")
        headers.setdefault("DNT", "1")
        headers.setdefault("Upgrade-Insecure-Requests", "1")

        kwargs["headers"] = headers
        self.logger.debug(f"Set User-Agent: {user_agent}")

        return url, kwargs

    def process_response(self, response, **kwargs):
        return response