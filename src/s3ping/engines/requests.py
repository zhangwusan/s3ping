import requests
from src.s3ping.types.base import ResponseType, RequestType
from src.s3ping.engines.base import BaseEngine

class RequestsEngine(BaseEngine):
    def send(self, request: RequestType) -> ResponseType:
        response = requests.request(
            method=request.get("method", "GET"),
            url=request["url"],
            headers=request.get("headers"),
            params=request.get("params"),
            data=request.get("data"),
            timeout=request.get("timeout", 10),
        )
        return response