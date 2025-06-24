from typing import Optional, Type, List
from src.s3ping.core.scrapers.base import BaseScraper
from src.s3ping.core.parsers.base import BaseParser
from src.s3ping.core.exporters.base import BaseExporter
from src.s3ping.types.base import RequestType
from src.s3ping.responses.html import HTMLResponse

class DefaultScraper(BaseScraper):
    def __init__(
        self,
        *args,
        parser: Optional[Type[BaseParser]] = None,  # parser class
        exporter: Optional[BaseExporter] = None,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.parser_class = parser
        self.exporter = exporter

    def run(self) -> None:
        urls: List[str] = self.config.get("urls", [])
        results = []

        for url in urls:
            request: RequestType = {"url": url, "method": "GET"}
            response: Optional[HTMLResponse] = self.request(request)

            if response is None:
                self.logger.error(f"No response received for {url}", caller=self)
                continue

            if self.parser_class:
                parser = self.parser_class(response)  # instantiate parser here with response
                parsed = parser.parse()
                results.append(parsed)

        if self.exporter:
            self.exporter.export(results)
        else:
            for r in results:
                self.logger.info(r)