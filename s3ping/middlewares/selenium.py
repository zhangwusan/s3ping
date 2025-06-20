import time
from typing import Optional, Dict, Any
from requests.models import Response
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from s3ping.middlewares.base import BaseMiddleware
from s3ping.s3ping.core.utils.logger import Logger

class SeleniumMiddleware(BaseMiddleware):
    def __init__(self, driver_path: Optional[str] = None, headless: bool = True, logger: Logger = None):
        super().__init__()
        self.logger = Logger(class_name=self.__class__.__name__)  # Automatically uses class name

        options = Options()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")

        service = Service(driver_path) if driver_path else None
        try:
            self.driver = webdriver.Chrome(service=service, options=options)
            self.logger.info("Initialized Selenium WebDriver")
        except Exception as e:
            self.logger.error(f"Failed to initialize WebDriver: {e}")
            self.driver = None

    def process_request(self, url: str, kwargs: Dict[str, Any]) -> Optional[str]:
        if not self.driver:
            self.logger.error("WebDriver not initialized.")
            return None

        self.logger.info(f"Fetching URL: {url}")
        try:
            self.driver.get(url)
            wait_time = kwargs.get("wait_time", 3)
            time.sleep(wait_time)
            return self.driver.page_source
        except Exception as e:
            self.logger.error(f"Error during page fetch: {e}")
            return None

    def process_response(self, response: Optional[Response], **kwargs) -> Optional[Response]:
        return response 

    def close(self):
        if self.driver:
            try:
                self.driver.quit()
                self.logger.info("Selenium WebDriver closed")
            except Exception as e:
                self.logger.error(f"Error closing Selenium WebDriver: {e}")

    def __del__(self):
        self.close()