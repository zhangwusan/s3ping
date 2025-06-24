# src/s3ping/scrapers/base.py
from abc import ABC, abstractmethod
from typing import Dict, Optional
from src.s3ping.loggers.logger import Logger
from src.s3ping.middlewares.manager import MiddlewareManager
from src.s3ping.types.base import RequestType, ResponseType
from src.s3ping.engines.base import BaseEngine

class BaseScraper(ABC):
    def __init__(
        self,
        engine: BaseEngine,
        middleware: MiddlewareManager,
        logger: Optional[Logger] = None,
        config: Optional[Dict] = None,
    ):
        self.engine = engine
        self.middleware = middleware
        self.logger = logger
        self.config = config or {}

    def request(self, req: RequestType) -> ResponseType:
        """Request → Middleware → Engine → Response."""
        self.logger.info(f"[Request] → {req['url']}", caller=self)
        response = self.middleware.execute(req, self.engine.send)
        self.logger.info(f"[Response] ← Status {getattr(response, 'status_code', 'N/A')}", caller=self)
        return response

    @abstractmethod
    def run(self):
        """Main scrape loop or entrypoint."""
        pass

    def parse(self, response: ResponseType):
        raise NotImplementedError("Override 'parse' in your subclass.")