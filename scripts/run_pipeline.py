import os
import sys
from typing import Dict, Any

# Add src/ to path for module resolution
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.s3ping.utils.load import load_config
from src.s3ping.core.scrapers.default import DefaultScraper
from src.s3ping.registry import (
    ENGINE_MAP,
    EXPORTER_REGISTRY,
    MIDDLEWARE_REGISTRY,
    PARSER_REGISTRY,
)
from src.s3ping.core.pipelines.base import BasePipeline


def build_pipeline(config: Dict[str, Any]) -> BasePipeline:
    # Load middlewares
    middlewares = []
    for name in config.get("middlewares", []):
        middleware_cls = MIDDLEWARE_REGISTRY.get(name)
        if not middleware_cls:
            raise ValueError(f"Middleware '{name}' not found in registry.")
        middlewares.append(middleware_cls())

    # Load parser
    parser_name = config.get("parser")
    parser_cls = PARSER_REGISTRY.get(parser_name)
    if not parser_cls:
        raise ValueError(f"Parser '{parser_name}' not found in registry.")
    parser = parser_cls

    # Load exporter
    exporter_config = config.get("exporter", {})
    exporter_name = exporter_config.get("name")
    exporter_path = exporter_config.get("path")
    exporter_factory = EXPORTER_REGISTRY.get(exporter_name)
    if not exporter_factory:
        raise ValueError(f"Exporter '{exporter_name}' not found in registry.")
    exporter = exporter_factory(exporter_path)

    # Load engine type
    engine_key = config.get("engine", "requests")
    engine_type = ENGINE_MAP.get(engine_key)
    if not engine_type:
        raise ValueError(f"Engine '{engine_key}' not found in ENGINE_MAP.")
    
    # Scrapper 

    # Build pipeline
    return BasePipeline(
        scraper_class=DefaultScraper,
        middlewares=middlewares,
        engine_type=engine_type,
        parser=parser,
        exporter=exporter,
        config=config,
    )


if __name__ == "__main__":
    config = load_config("./src/s3ping/config/scrapes/default.yaml")  # must return a dict
    pipeline = build_pipeline(config)
    pipeline.run()