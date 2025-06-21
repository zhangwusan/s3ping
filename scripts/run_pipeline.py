from s3ping.core.utils.logger import Logger
from s3ping.core.exporter.default import JsonExporter
from s3ping.core.parser.default import DefaultParser
from s3ping.core.pipeline.scrape import ScraperPipeline
from s3ping.middlewares.proxy import ProxyMiddleware
from s3ping.middlewares.retry import RetryMiddleware
from s3ping.middlewares.header import HeaderMiddleware
from s3ping.middlewares.captcha import CaptchaMiddleware
from s3ping.middlewares.selenium import SeleniumMiddleware


def run_default_pipeline():
    url = "https://news.sabay.com.kh/"
    logger = Logger(log_file_name="default_pipeline.log")

    pipeline = ScraperPipeline(
        url=url,
        middlewares=[
            HeaderMiddleware(randomize=True, logger=logger),
            ProxyMiddleware(logger=logger),
        ],
        parser=DefaultParser(),
        exporter=JsonExporter(filepath="output/default.json"),
        logger=logger,
    )

    pipeline.run()


def run_retry_pipeline():
    url = "https://news.sabay.com.kh/"
    logger = Logger(log_file_name="logs/retry_pipeline.log")

    pipeline = ScraperPipeline(
        url=url,
        middlewares=[
            HeaderMiddleware(randomize=True, logger=logger),
            ProxyMiddleware(logger=logger),
            RetryMiddleware(max_retries=3, delay=2, backoff=2, logger=logger),
        ],
        parser=DefaultParser(),
        exporter=JsonExporter(filepath="output/retry.json"),
        logger=logger,
    )

    pipeline.run()


def run_full_pipeline_with_selenium():
    url = "https://news.sabay.com.kh/"
    logger = Logger(log_file_name="selenium_pipeline.log")

    pipeline = ScraperPipeline(
        url=url,
        middlewares=[
            HeaderMiddleware(randomize=True, logger=logger),
            ProxyMiddleware(logger=logger),
            CaptchaMiddleware(auto_solve=False, logger=logger),
            RetryMiddleware(max_retries=2, delay=1, backoff=1.5, logger=logger),
            SeleniumMiddleware(driver_path=None, headless=True, logger=logger),
        ],
        parser=DefaultParser(),
        exporter=JsonExporter(filepath="output/selenium.json"),
        logger=logger,
    )

    pipeline.run()


if __name__ == "__main__":
    run_default_pipeline()
    # run_retry_pipeline()
    # run_full_pipeline_with_selenium()