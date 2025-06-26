from typing import Dict, Any
from src.s3ping.core.pipelines.base import BasePipeline
from src.s3ping.registry import (
    ENGINE_MAP,
    EXPORTER_REGISTRY,
    MIDDLEWARE_REGISTRY,
    PARSER_REGISTRY,
    SCRAPER_REGISTRY,
)

def build_pipeline(config: Dict[str, Any]) -> BasePipeline:
    # Get scraper
    scraper_name = config.get("scraper", "DefaultScraper")
    scraper_class = SCRAPER_REGISTRY.get(scraper_name)
    if not scraper_class:
        raise ValueError(f"Scraper '{scraper_name}' not found in SCRAPER_REGISTRY")

    # Get middlewares
    middlewares = []
    for m in config.get("middlewares", []):
        name = m["name"] if isinstance(m, dict) else m
        params = m.get("params", {}) if isinstance(m, dict) else {}
        middleware_cls = MIDDLEWARE_REGISTRY.get(name)
        if not middleware_cls:
            raise ValueError(f"Middleware '{name}' not found in MIDDLEWARE_REGISTRY")
        middlewares.append(middleware_cls(**params))

    # Get parser class (optional)
    parser = None
    parser_cfg = config.get("parser")
    if parser_cfg:
        parser_name = parser_cfg.get("name") if isinstance(parser_cfg, dict) else parser_cfg
        parser_class = PARSER_REGISTRY.get(parser_name)
        if not parser_class:
            raise ValueError(f"Parser '{parser_name}' not found in PARSER_REGISTRY")
        parser = parser_class

    # Get exporter (instantiated)
    exporter = None
    exporter_cfg = config.get("exporter")
    if exporter_cfg:
        exporter_name = exporter_cfg.get("name")
        exporter_params = exporter_cfg.get("params", {})
        exporter_factory = EXPORTER_REGISTRY.get(exporter_name)
        if not exporter_factory:
            raise ValueError(f"Exporter '{exporter_name}' not found in EXPORTER_REGISTRY")
        exporter = exporter_factory(**exporter_params)

    # Get engine type
    engine_key = config.get("engine", "requests")
    engine_type = ENGINE_MAP.get(engine_key)
    if not engine_type:
        raise ValueError(f"Engine '{engine_key}' not found in ENGINE_MAP")

    # Return pipeline
    return BasePipeline(
        scraper_class=scraper_class,
        middlewares=middlewares,
        engine_type=engine_type,
        parser=parser,
        exporter=exporter,
        config=config,
    )