from abc import ABC, abstractmethod
from typing import Dict, Optional, Any
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
        config: Optional[Dict[str, Any]] = None,
    ):
        self.engine: BaseEngine = engine
        self.middleware: MiddlewareManager = middleware
        self.logger: Optional[Logger] = logger
        self.config: Dict[str, Any] = config or {}

    def request(self, req: RequestType) -> ResponseType:
        """Request → Middleware → Engine → Response."""
        if self.logger:
            self.logger.info(f"[Request] → {req['url']}", caller=self)
        response = self.middleware.execute(req, self.engine.send)
        if self.logger:
            self.logger.info(f"[Response] ← Status {getattr(response, 'status_code', 'N/A')}", caller=self)
        return response

    @abstractmethod
    def run(self) -> None:
        """Main scrape loop or entrypoint."""
        pass

    def parse(self, response: ResponseType) -> Any:
        """Override this method in subclasses if parsing is needed."""
        raise NotImplementedError("Override 'parse' in your subclass.")