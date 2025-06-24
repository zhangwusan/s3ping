from typing import Optional, List, Dict, Tuple, Union
import cloudscraper
from requests.models import Response
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
        self.logger = logger or Logger(class_name=self.__class__.__name__)
        self.scraper = cloudscraper.create_scraper()
        self.middlewares = middlewares or []

    def fetch(self, url: str, **kwargs) -> Optional[Union[str, List[str]]]:
        scroll = kwargs.get("scroll", False)
        scroll_limit = kwargs.get("scroll_limit", 1)

        for mw in self.middlewares:
            result = mw.process_request(url, kwargs)
            if isinstance(result, tuple):
                url, kwargs = result
            elif result is None:
                self.logger.warning(f"{mw.__class__.__name__} aborted the request.")
                return None

        for mw in self.middlewares:
            if hasattr(mw, "fetch") and hasattr(mw, "scroll_step") and hasattr(mw, "get_content"):
                try:
                    mw.fetch(url, kwargs)

                    if not scroll:
                        return mw.get_content()

                    self.logger.info(f"Scroll mode: {scroll_limit} iterations")
                    all_pages = []
                    for i in range(scroll_limit):
                        content = mw.get_content()
                        all_pages.append(content)

                        if not mw.scroll_step(i):
                            self.logger.info(f"Stopped scroll at {i}")
                            break

                    return all_pages

                except Exception as e:
                    self.logger.error(f"{mw.__class__.__name__} failed: {e}")

        # fallback: cloudscraper
        try:
            self.logger.info(f"Fetching via cloudscraper: {url}")
            allowed_keys = {"headers", "params", "data", "json", "proxies", "auth", "cookies"}
            filtered_kwargs = {k: v for k, v in kwargs.items() if k in allowed_keys}
            response = self.scraper.get(url, timeout=self.timeout, **filtered_kwargs)
            response.raise_for_status()
            return response.text
        except Exception as e:
            self.logger.error(f"Request failed: {e}")
            return None
