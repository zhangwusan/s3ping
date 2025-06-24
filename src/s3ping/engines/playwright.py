from src.s3ping.types.base import RequestType, ResponseType
from src.s3ping.engines.base import BaseEngine
import requests
from playwright.sync_api import sync_playwright

class PlaywrightEngine(BaseEngine):
    def send(self, request: RequestType) -> ResponseType:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(request["url"])
            content = page.content()
            browser.close()
            return requests.Response() 