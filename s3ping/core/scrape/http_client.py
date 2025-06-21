from typing import Optional, List, Dict, Tuple, Union
import cloudscraper
from s3ping.middlewares.base import BaseMiddleware
from s3ping.core.utils.logger import Logger

class HttpClient:
    def __init__(
        self,
        middlewares: Optional[List[BaseMiddleware]] = None,
        timeout: int = 15,
        logger: Optional[Logger] = None,
    ):
        self.timeout = timeout
        self.logger = logger
        self.scraper = cloudscraper.create_scraper()
        self.middlewares = middlewares or []

    def fetch(self, url: str, **kwargs) -> Optional[str]:
        # Step 1: Preprocess request via middleware
        for mw in self.middlewares:
            result = mw.process_request(url, kwargs)
            if isinstance(result, tuple):
                url, kwargs = result
            elif result is None:
                if self.logger:
                    self.logger.warning(f"{mw.__class__.__name__} aborted the request.")
                return None
            else:
                self.logger.warning(f"{mw.__class__.__name__} returned unexpected value: {type(result)}")

        # Step 2: Attempt fetch via middleware (SeleniumMiddleware preferred)
        response = None
        for mw in self.middlewares:
            if hasattr(mw, "fetch") and callable(getattr(mw, "fetch")):
                if self.logger:
                    self.logger.info(f"Trying fetch with middleware: {mw.__class__.__name__}")
                response = mw.fetch(url, kwargs)
                if response is not None:
                    break  # first successful fetch stops the loop

        # Step 3: Default to cloudscraper fetch if no middleware did it
        if response is None:
            if self.logger:
                self.logger.info(f"Fetching with default cloudscraper: {url}")
            try:
                response = self.scraper.get(url, timeout=self.timeout, **kwargs)
                response.raise_for_status()
            except Exception as e:
                if self.logger:
                    self.logger.error(f"Request failed: {e}")
                return None

        # Step 4: Post-process response via middleware
        for mw in reversed(self.middlewares):
            response = mw.process_response(response)
            if response is None:
                if self.logger:
                    self.logger.warning(f"{mw.__class__.__name__} blocked the response.")
                return None

        return response.text