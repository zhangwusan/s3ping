from typing import List, Optional, Any, Dict
from s3ping.core.scrape.http_client import HttpClient
from s3ping.core.utils.logger import Logger
from s3ping.middlewares.header import HeaderMiddleware
from s3ping.core.exporter.base import BaseExporter
from s3ping.core.parser.base import BaseParser
from s3ping.core.parser.default import DefaultParser
import traceback


class ScraperPipeline:
    def __init__(
        self,
        url: str,
        middlewares: Optional[List] = None,
        parser: Optional[BaseParser] = None,
        exporter: Optional[BaseExporter] = None,
        logger: Optional[Logger] = None,
        debug: bool = True,
        http_timeout: int = 15,
    ):
        self.url = url
        self.debug = debug
        self.parser = parser or DefaultParser()
        self.logger = logger or Logger(log_paths=['logs/pipeline.log'], class_name=self.__class__.__name__)
        self.exporter = exporter

        self.client = HttpClient(
            middlewares=middlewares or [HeaderMiddleware(randomize=False, logger=self.logger)],
            timeout=http_timeout,
            logger=self.logger
        )

    def run(self, **kwargs) -> Any:
        try:
            self.logger.info(f"Starting pipeline for: {self.url}")
            content = self.client.fetch(self.url, **kwargs)

            if not content:
                self.logger.error("Failed to fetch content.")
                return None

            self.logger.info("Parsing content...")
            data = self.parser.parse(content)
            self.logger.info(data)

            if self.exporter:
                self.logger.info("Exporting data...")
                self.exporter.export(data)
            else:
                self.logger.info("No exporter provided. Skipping export.")

            self.logger.info("Pipeline finished successfully.")
            return data

        except Exception as e:
            if self.debug:
                self.logger.critical("Pipeline crashed:\n" + traceback.format_exc())
            else:
                self.logger.error(f"Unexpected error: {e}")
            return None

    @classmethod
    def from_config(cls, config: Dict[str, Any]) -> "ScraperPipeline":
        return cls(
            url=config.get("url"),
            parser=config.get("parser"),
            exporter=config.get("exporter"),
            middlewares=config.get("middlewares"),
            logger=config.get("logger"),
            debug=config.get("debug", True),
            http_timeout=config.get("http_timeout", 15),
        )