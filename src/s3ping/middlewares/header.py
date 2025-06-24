import random
from src.s3ping.types.base import NextHandlerType, RequestType, ResponseType
from src.s3ping.middlewares.base import BaseMiddleware

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (X11; Linux x86_64)",
]

class HeaderMiddleware(BaseMiddleware):
    def __init__(self, user_agent: str = None, logger=None):
        super().__init__(logger=logger)
        self.user_agent = user_agent

    def process(self, request: RequestType, next: NextHandlerType) -> ResponseType:
        ua = self.user_agent or random.choice(USER_AGENTS)
        request.setdefault("headers", {})["User-Agent"] = ua
        if self.logger:
            self.logger.debug(f"HeaderMiddleware set User-Agent: {ua}", caller=self)
        return next(request)