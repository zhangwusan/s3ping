from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from src.s3ping.responses.html import HTMLResponse
from src.s3ping.types.base import RequestType, ResponseType
from src.s3ping.engines.base import BaseEngine


class SeleniumEngine(BaseEngine):
    def __init__(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(options=options)

    def send(self, request: RequestType) -> ResponseType:
        self.driver.get(request["url"])
        content = self.driver.page_source
        return HTMLResponse(content=content, url=request["url"])

    def __del__(self):
        if hasattr(self, "driver"):
            self.driver.quit()