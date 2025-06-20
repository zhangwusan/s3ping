import time
import functools
from typing import Callable, Optional, Type, Tuple, Any, Dict
from s3ping.middlewares.base import BaseMiddleware
from s3ping.core.utils.logger import Logger


class RetryMiddleware(BaseMiddleware):
    def __init__(
        self,
        exceptions: Tuple[Type[BaseException], ...] = (Exception,),
        max_retries: int = 3,
        delay: float = 1.0,
        backoff: float = 2.0,
        logger: Logger = None
    ):
        super().__init__()
        self.logger = Logger(class_name=self.__class__.__name__)
        self.exceptions = exceptions
        self.max_retries = max_retries
        self.delay = delay
        self.backoff = backoff

        self.logger.info(
            f"Initialized with max_retries={self.max_retries}, delay={self.delay}, backoff={self.backoff}"
        )

    def __call__(self, func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            current_delay = self.delay
            while retries <= self.max_retries:
                try:
                    return func(*args, **kwargs)
                except self.exceptions as e:
                    retries += 1
                    self.logger.warning(f"Retry {retries}/{self.max_retries} due to: {e}")
                    if retries > self.max_retries:
                        self.logger.error(f"Exceeded max retries: {self.max_retries}")
                        raise
                    time.sleep(current_delay)
                    current_delay *= self.backoff
        return wrapper

    def process_request(self, url: str, kwargs: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
        return url, kwargs

    def process_response(self, response: Optional[Any], **kwargs) -> Optional[Any]:
        return response