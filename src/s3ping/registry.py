from typing import Dict, Any, List, Type
from src.s3ping.core.pipelines.base import BasePipeline
from src.s3ping.core.parsers.base import BaseParser
from src.s3ping.core.exporters.base import BaseExporter
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
}

EXPORTER_REGISTRY: Dict[str, Any] = {
    "JsonExporter": lambda output_path=None, **kwargs: JsonExporter(output_path=output_path),
}

MIDDLEWARE_REGISTRY: Dict[str, Type[BaseMiddleware]] = {
    "HeaderMiddleware": HeaderMiddleware,
    "RetryMiddleware": RetryMiddleware,
}

ENGINE_MAP: Dict[str, EngineType] = {
    "requests": EngineType.REQUESTS,
    "selenium": EngineType.SELENIUM,
}

def build_pipeline(config: Dict[str, Any]) -> BasePipeline:
    # Scraper class
    scraper_name = config.get("scraper", "DefaultScraper")
    scraper_class = SCRAPER_REGISTRY.get(scraper_name)
    if not scraper_class:
        raise ValueError(f"Scraper '{scraper_name}' not found")

    # Middlewares list
    middlewares_cfg = config.get("middlewares", [])
    middlewares: List[BaseMiddleware] = []
    for m_cfg in middlewares_cfg:
        if isinstance(m_cfg, dict):
            name = m_cfg.get("name")
            params = m_cfg.get("params", {})
        else:
            name = m_cfg
            params = {}
        m_cls = MIDDLEWARE_REGISTRY.get(name)
        if not m_cls:
            raise ValueError(f"Middleware '{name}' not found")
        middlewares.append(m_cls(**params))

    # Parser (pass the class, don't instantiate)
    parser_cfg = config.get("parser", {})
    if isinstance(parser_cfg, dict):
        parser_name = parser_cfg.get("name")
    else:
        parser_name = parser_cfg

    parser_class = PARSER_REGISTRY.get(parser_name)
    if not parser_class:
        raise ValueError(f"Parser '{parser_name}' not found")

    # Exporter
    exporter_cfg = config.get("exporter", {})
    if exporter_cfg:
        if isinstance(exporter_cfg, dict):
            exporter_name = exporter_cfg.get("name")
            exporter_params = exporter_cfg.get("params", {})
        else:
            exporter_name = exporter_cfg
            exporter_params = {}

        exporter_factory = EXPORTER_REGISTRY.get(exporter_name)
        if not exporter_factory:
            raise ValueError(f"Exporter '{exporter_name}' not found")
        exporter_instance = exporter_factory(**exporter_params)
    else:
        exporter_instance = None

    # Engine
    engine_key = config.get("engine", "requests")
    engine_type = ENGINE_MAP.get(engine_key)
    if not engine_type:
        raise ValueError(f"Engine '{engine_key}' not found")

    # Build pipeline
    pipeline = BasePipeline(
        scraper_class=scraper_class,
        middlewares=middlewares,
        engine_type=engine_type,
        parser=parser_class,  # pass parser class here
        exporter=exporter_instance,
        config=config,
    )
    return pipeline