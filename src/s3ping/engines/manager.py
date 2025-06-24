from typing import Optional
from src.s3ping.constants.engine import EngineType
from src.s3ping.types.base import RequestType, ResponseType
from src.s3ping.engines.base import BaseEngine
from src.s3ping.engines.requests import RequestsEngine
from src.s3ping.engines.cloudscraper import CloudscraperEngine
from src.s3ping.engines.playwright import PlaywrightEngine
from src.s3ping.engines.selenium import SeleniumEngine


class EngineManager:
    def __init__(self, engine_type: EngineType, logger=None):
        self.logger = logger
        self.engine: Optional[BaseEngine] = self._select_engine(engine_type)

    def _select_engine(self, engine_type: EngineType) -> BaseEngine:
        if engine_type == EngineType.REQUESTS:
            if self.logger:
                self.logger.info("Using RequestsEngine", caller=self)
            return RequestsEngine(logger=self.logger)
        elif engine_type == EngineType.CLOUDSCRAPER:
            if self.logger:
                self.logger.info("Using CloudscraperEngine", caller=self)
            return CloudscraperEngine()
        elif engine_type == EngineType.PLAYWRIGHT:
            if self.logger:
                self.logger.info("Using PlaywrightEngine", caller=self)
            return PlaywrightEngine()
        elif engine_type == EngineType.SELENIUM:
            if self.logger:
                self.logger.info("Using SeleniumEngine", caller=self)
            return SeleniumEngine()
        else:
            raise ValueError(f"Unknown engine type: {engine_type}")

    def send(self, request: RequestType) -> ResponseType:
        if not self.engine:
            raise RuntimeError("No engine initialized")
        if self.logger:
            self.logger.debug(f"Sending request via {self.engine.__class__.__name__}: {request['url']}", caller=self)
        return self.engine.send(request)