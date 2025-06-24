import cloudscraper
from src.s3ping.types.base import RequestType, ResponseType
from src.s3ping.engines.base import BaseEngine

class CloudscraperEngine(BaseEngine):
    def __init__(self):
        self.scraper = cloudscraper.create_scraper()

    def send(self, request: RequestType) -> ResponseType:
        return self.scraper.request(
            method=request.get("method", "GET"),
            url=request["url"],
            headers=request.get("headers"),
            params=request.get("params"),
            data=request.get("data"),
            timeout=request.get("timeout", 10),
        )