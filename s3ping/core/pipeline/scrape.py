from typing import List, Optional, Any
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
    ):
        self.url = url
        self.debug = debug
        self.parser = parser or DefaultParser()
        self.logger = logger or Logger(log_paths=['logs/pipeline/process.log'], class_name=self.__class__.__name__)
        self.exporter = exporter

        self.client = HttpClient(
            middlewares=middlewares or [HeaderMiddleware(randomize=False, logger=self.logger)],
            logger=self.logger
        )

    def run(self) -> Any:
        try:
            self.logger.info(f"Starting pipeline for: {self.url}")
            content = self.client.fetch(self.url)

            if not content:
                self.logger.error("Failed to fetch content")
                return None

            self.logger.info("Parsing content...")
            data = self.parser.parse(content)

            if self.exporter:
                self.logger.info("Exporting data...")
                self.exporter.export(data)
            else:
                self.logger.info("No exporter defined, skipping export.")

            self.logger.info("Pipeline completed successfully")
            return data

        except Exception as e:
            if self.debug:
                self.logger.critical("Pipeline crashed with an unhandled exception:\n" + traceback.format_exc())
            else:
                self.logger.error(f"Unexpected error: {e}")
            return None