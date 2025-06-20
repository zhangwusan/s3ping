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
        # Process request middleware
        for mw in self.middlewares:
            result: Union[Tuple[str, Dict], str, None] = mw.process_request(url, kwargs)
            if isinstance(result, tuple):
                url, kwargs = result
            elif isinstance(result, str):
                # Middleware returned HTML content directly (e.g. SeleniumMiddleware)
                if self.logger:
                    self.logger.info(f"Middleware {mw.__class__.__name__} returned content directly")
                return result
            elif result is None:
                # Middleware indicates to stop fetching
                if self.logger:
                    self.logger.warning(f"Middleware {mw.__class__.__name__} returned None, aborting fetch")
                return None
            else:
                if self.logger:
                    self.logger.warning(f"[Logger] Middleware {mw.__class__.__name__} returned unexpected type: {type(result)}")

        if self.logger:
            self.logger.info(f"Sending request to {url}")

        try:
            response = self.scraper.get(url, timeout=self.timeout, **kwargs)
            response.raise_for_status()
        except Exception as e:
            if self.logger:
                self.logger.error(f"Request failed: {e}")
            raise

        # Process response middleware
        for mw in reversed(self.middlewares):
            modified_response = mw.process_response(response)
            if modified_response is None:
                if self.logger:
                    self.logger.warning(f"Middleware {mw.__class__.__name__} returned None response. Aborting.")
                return None
            response = modified_response

        return response.text