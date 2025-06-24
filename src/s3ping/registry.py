from src.s3ping.core.exporters.json import JsonExporter
from src.s3ping.core.parsers.default import DefaultParser
from src.s3ping.middlewares.header import HeaderMiddleware
from src.s3ping.middlewares.retry import RetryMiddleware
from src.s3ping.constants.engine import EngineType

MIDDLEWARE_REGISTRY = {
    "HeaderMiddleware": HeaderMiddleware,
    "RetryMiddleware": RetryMiddleware,
}

PARSER_REGISTRY = {
    "DefaultParser": DefaultParser,
}

EXPORTER_REGISTRY = {
    "JsonExporter": lambda path: JsonExporter(output_path=path),
}

ENGINE_MAP = {
    "requests": EngineType.REQUESTS,
    "cloudscraper": EngineType.CLOUDSCRAPER,
    "playwright": EngineType.PLAYWRIGHT,
    "selenium": EngineType.SELENIUM,
}