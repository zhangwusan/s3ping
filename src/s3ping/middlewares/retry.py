import time
from typing import List
from src.s3ping.types.base import NextHandlerType, RequestType, ResponseType
from src.s3ping.constants.http_status import HTTPStatus
from src.s3ping.middlewares.base import BaseMiddleware

class RetryMiddleware(BaseMiddleware):
    def __init__(
        self,
        retries: int = 3,
        delay: float = 1.0,
        retry_on: List[int] = None,
        logger=None
    ):
        super().__init__(logger=logger)
        self.retries = retries
        self.delay = delay
        self.retry_on = retry_on or [
            HTTPStatus.TOO_MANY_REQUESTS,
            HTTPStatus.INTERNAL_SERVER_ERROR,
            HTTPStatus.BAD_GATEWAY,
            HTTPStatus.SERVICE_UNAVAILABLE,
            HTTPStatus.GATEWAY_TIMEOUT,
        ]

    def process(self, request: RequestType, next: NextHandlerType) -> ResponseType:
        attempt = 0
        while attempt <= self.retries:
            try:
                response = next(request)
                # Check if response status is in retry list
                if response is None:
                    # No response, retry
                    raise Exception("No response received")
                status_code = getattr(response, "status_code", None)
                if status_code in self.retry_on:
                    self.logger.warning(f"Retryable status {status_code} received, retrying...", caller=self)
                    attempt += 1
                    if attempt <= self.retries:
                        time.sleep(self.delay)
                    continue  # retry again
                # Success response
                return response
            except Exception as e:
                self.logger.warning(f"Exception during request: {e}. Retrying...", caller=self)
                attempt += 1
                if attempt <= self.retries:
                    time.sleep(self.delay)
        # After retries exhausted, last attempt without retry
        return next(request)