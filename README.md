# s3ping

[![PyPI version](https://img.shields.io/pypi/v/s3ping.svg)](https://pypi.org/project/s3ping)
[![Python Version](https://img.shields.io/pypi/pyversions/s3ping.svg)](https://pypi.org/project/s3ping)
[![License](https://img.shields.io/pypi/l/s3ping.svg)](LICENSE)

`s3ping` is a lightweight, flexible Python library designed for efficient and customizable web scraping. It provides tools to easily parse HTML content, handle dynamic CSS selectors, and manage scraping pipelines with logging and export capabilities.

---

## Features

- Simple HTML parsing using CSS selectors with support for fallback selectors.
- Utilities for extracting text and attributes safely.
- Extensible scraping pipeline for URL fetching, parsing, logging, and exporting results.
- Built-in support for logging with colored console output and multiple log files.
- Export scraped data to JSON or other formats.
- Designed to be modular and easy to extend for various scraping needs.

---

## Installation

```bash
pip install s3ping
```

## Quick Start

```python
from s3ping.core.parser.base import BaseParser
from s3ping.core.parser.html import HtmlParser
from s3ping.core.utils.logger import Logger
from typing import Any, Optional
from s3ping.core.pipeline.scrape import ScraperPipeline
from s3ping.core.utils.logger import Logger
from s3ping.core.export.json_exporter import JsonExporter


class DefaultParser(BaseParser):
    def __init__(self, logger: Optional[Logger] = None):
        self.logger = logger

    def parse(self, content: str) -> Any:
        if self.logger:
            self.logger.info("Parsing general content...")

        parser = HtmlParser(content)

        links = parser.extract_links(selectors=["a"])
        images = parser.extract_images(selectors=["img"])
        headings = parser.get_all_texts("h1, h2, h3, h4, h5, h6")

        return {
            "links": links,
            "images": images,
            "headings": headings,
        }

def main():
    logger = Logger(log_paths=["logs/default_parse.log"])
    pipeline = ScraperPipeline(
        url="https://example.com",
        parser=DefaultParser(logger=logger),
        logger=logger,
        exporter=JsonExporter(filepath="output/general_data.json"),
        debug=True,
    )

    result = pipeline.run()
    if result:
        logger.info("Scraping finished.")
        for key, items in result.items():
            print(f"\n{key.upper()}")
            for item in items:
                print(item)
    else:
        logger.error("Scraping failed.")


if __name__ == "__main__":
    main()
```