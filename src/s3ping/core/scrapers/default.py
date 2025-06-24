from typing import Optional, Type
from src.s3ping.core.parsers.default import DefaultParser
from src.s3ping.core.scrapers.base import BaseScraper
from src.s3ping.core.parsers.base import BaseParser
from src.s3ping.core.exporters.base import BaseExporter

class DefaultScraper(BaseScraper):
    def __init__(
        self,
        engine,
        middleware,
        logger=None,
        config=None,
        parser: Optional[Type[BaseParser]] = None,
        exporter: Optional[BaseExporter] = None,
    ):
        super().__init__(engine, middleware, logger, config)
        self.parser_class = parser or DefaultParser
        self.exporter = exporter

    def run(self) -> None:
        urls = self.config.get("urls", [])
        results = []

        for url in urls:
            request = {"url": url, "method": "GET"}
            response = self.request(request)

            if self.parser_class:
                parser = self.parser_class(response)
                parsed = parser.parse()
                results.extend(parsed)

        if self.exporter:
            self.exporter.export(results)
        else:
            for r in results:
                self.logger.info(r)