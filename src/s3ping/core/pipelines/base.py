from typing import Type, Optional, List, Dict, Any, Union
from src.s3ping.constants.engine import EngineType
from src.s3ping.loggers.logger import Logger
from src.s3ping.core.scrapers.base import BaseScraper
from src.s3ping.middlewares.base import BaseMiddleware
from src.s3ping.middlewares.manager import MiddlewareManager
from src.s3ping.engines.base import BaseEngine
from src.s3ping.engines.manager import EngineManager

class BasePipeline:
    def __init__(
        self,
        scraper_class: Type[BaseScraper],
        middlewares: Optional[List[BaseMiddleware]] = None,
        engine: Optional[BaseEngine] = None,
        engine_type: Optional[EngineType] = None,
        logger: Optional[Logger] = None,
        config: Optional[Dict[str, Any]] = None,
    ):
        self.logger = logger or Logger(class_name=self.__class__.__name__)
        
        # Use engine instance if provided, else create engine by type via EngineManager
        if engine:
            self.engine = engine
        else:
            etype = engine_type or EngineType.REQUESTS
            self.engine_manager = EngineManager(engine_type=etype, logger=self.logger)
            self.engine = self.engine_manager.engine
        
        self.middleware = MiddlewareManager(middlewares or [])
        self.scraper_class = scraper_class
        self.config = config or {}

    def run(self) -> None:
        scraper = self.scraper_class(
            engine=self.engine,
            middleware=self.middleware,
            logger=self.logger,
            config=self.config
        )
        self.logger.info(f"Running scraper: {self.scraper_class.__name__}", caller=self)
        scraper.run()