from ast import parse
import os

from dotenv import load_dotenv
from s3ping.core.parser.base import BaseParser
from s3ping.core.parser.html import HtmlParser
from typing import Any, Optional

from s3ping.core.utils.logger import Logger
from s3ping.core.pipeline.scrape import ScraperPipeline
from s3ping.core.exporter.default import JsonExporter

from s3ping.middlewares.selenium import SeleniumMiddleware
from s3ping.middlewares.captcha import CaptchaMiddleware
from s3ping.solvers.capsolver import CapSolver

load_dotenv()
api_key = os.getenv("CAPSOLVER_API_KEY")


class NewsParser(BaseParser):
    def __init__(self, logger: Optional[Logger] = None):
        super().__init__()
        self.logger = logger

    def parse(self, content: str) -> Any:
        if self.logger:
            self.logger.info("Parsing content...")

        parser = HtmlParser(content, parser='html.parser')
        # for element in parser.soup.find_all(True):  # True = match all tags
        #     print(f"<{element.name}> attributes: {element.attrs}")

        return parser


def main():
    logger = Logger(log_paths=["logs/main.log"])
    pipeline = ScraperPipeline(
        url="https://www.google.com/recaptcha/api2/demo",
        middlewares=[
            CaptchaMiddleware(auto_solve=True ,solver=CapSolver(api_key=api_key, logger=logger)),
            SeleniumMiddleware(driver_path='driver/chromedriver-mac-arm64/chromedriver', headless=True),
        ],
        parser=NewsParser(logger=logger),
        logger=logger,
        debug=True
    )

    result = pipeline.run()
    if result:
        logger.info("Scraping succeeded.")            
    else:
        logger.error("Failed to fetch.")


if __name__ == '__main__':
    main()