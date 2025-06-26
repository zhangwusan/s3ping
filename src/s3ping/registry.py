from typing import Dict, Any, Type
from src.s3ping.core.exporters.html import HtmlExporter
from src.s3ping.core.parsers.full import FullDOMParser
from src.s3ping.core.parsers.base import BaseParser
from src.s3ping.core.scrapers.base import BaseScraper
from src.s3ping.middlewares.base import BaseMiddleware
from src.s3ping.constants.engine import EngineType
from src.s3ping.core.parsers.default import DefaultParser
from src.s3ping.core.exporters.json import JsonExporter
from src.s3ping.core.scrapers.default import DefaultScraper
from src.s3ping.middlewares.header import HeaderMiddleware
from src.s3ping.middlewares.retry import RetryMiddleware


SCRAPER_REGISTRY: Dict[str, Type[BaseScraper]] = {
    "DefaultScraper": DefaultScraper,
}

PARSER_REGISTRY: Dict[str, Type[BaseParser]] = {
    "DefaultParser": DefaultParser,
    "FullDOMParser" : FullDOMParser
}

EXPORTER_REGISTRY: Dict[str, Any] = {
    "JsonExporter": lambda output_path=None, **kwargs: JsonExporter(output_path=output_path),
    "HtmlExporter": lambda output_path=None, **kwargs: HtmlExporter(output_path=output_path)
}

MIDDLEWARE_REGISTRY: Dict[str, Type[BaseMiddleware]] = {
    "HeaderMiddleware": HeaderMiddleware,
    "RetryMiddleware": RetryMiddleware,
}

ENGINE_MAP: Dict[str, EngineType] = {
    "requests": EngineType.REQUESTS,
    "selenium": EngineType.SELENIUM,
}