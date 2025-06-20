from s3ping.core.parser.base import BaseParser
from s3ping.core.parser.html import HtmlParser
from typing import Any, Optional

from s3ping.core.utils.logger import Logger
from s3ping.core.pipeline.scrape import ScraperPipeline
from s3ping.core.exporter.default import JsonExporter


class NewsParser(BaseParser):
    def __init__(self, logger: Optional[Logger] = None):
        super().__init__()
        self.logger = logger

    def parse(self, content: str) -> Any:
        if self.logger:
            self.logger.info("Parsing content...")

        parser = HtmlParser(content)
        nav_links = parser.find_all_elements("ul.nav.navbar-nav li a")

        results = []
        for link in nav_links:
            text = parser.extract_text(link)
            href = parser.extract_attribute(link, "href")
            if self.logger:
                self.logger.debug(f"Found link: {text} -> {href}")
            results.append({"label": text, "href": href})

        if self.logger:
            self.logger.info(f"Extracted {len(results)} nav links.")

        return results


def main():
    logger = Logger(log_paths=["logs/main.log"])
    pipeline = ScraperPipeline(
        url="https://news.sabay.com.kh/",
        parser=NewsParser(logger=logger),
        logger=logger,
        exporter=JsonExporter(filepath='output/news.json'),
        debug=True
    )

    result = pipeline.run()
    if result:
        logger.info("Scraping succeeded.")
        for item in result:
            print(item)
    else:
        logger.error("Failed to fetch.")


if __name__ == '__main__':
    main()