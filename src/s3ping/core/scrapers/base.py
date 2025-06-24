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
        self.logger: Logger = logger or Logger(class_name=self.__class__.__name__)
        self.config: Dict[str, Any] = config or {}

    def request(self, req: RequestType) -> Optional[ResponseType]:
        """Request → Middleware → Engine → Response."""
        self.logger.info(f"[Request] → {req['url']}", caller=self)
        try:
            response = self.middleware.execute(req, self.engine.send)
        except Exception as e:
            self.logger.error(f"Request failed: {e}", caller=self)
            return None

        if response is None:
            self.logger.error(f"No response received for {req['url']}", caller=self)
            return None

        self.logger.info(f"[Response] ← Status {getattr(response, 'status_code', 'N/A')}", caller=self)
        return response

    @abstractmethod
    def run(self) -> None:
        """Main scrape loop or entrypoint."""
        pass

    def parse(self, response: ResponseType) -> Any:
        """Override this method in subclasses if parsing is needed."""
        raise NotImplementedError("Override 'parse' in your subclass.")