import random
from typing import Dict, Any
from src.s3ping.types.base import NextHandlerType, RequestType, ResponseType
from src.s3ping.middlewares.base import BaseMiddleware

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (X11; Linux x86_64)",
]

class HeaderMiddleware(BaseMiddleware):
    def __init__(self, headers: Dict[str, str] = None, logger=None):
        super().__init__(logger=logger)
        self.headers = headers or {}

    def process(self, request: RequestType, next: NextHandlerType) -> ResponseType:
        # Ensure headers dict exists
        headers: Dict[str, Any] = request.setdefault("headers", {})

        # Randomize or override User-Agent
        if "User-Agent" not in headers:
            ua = random.choice(USER_AGENTS)
            headers["User-Agent"] = ua
            if self.logger:
                self.logger.debug(f"[HeaderMiddleware] Set User-Agent: {ua}", caller=self)

        # Inject default headers (e.g. Accept-Language, Referer, etc.)
        for key, value in self.headers.items():
            headers.setdefault(key, value)  # Don't override explicitly passed headers

        return next(request)