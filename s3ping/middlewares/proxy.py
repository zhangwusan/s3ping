from itertools import cycle
from typing import Optional, List, Dict, Tuple, Any
from requests.models import Response
from s3ping.s3ping.core.utils.logger import Logger
from s3ping.middlewares.base import BaseMiddleware


class ProxyMiddleware(BaseMiddleware):
    def __init__(
        self,
        proxies: Optional[List[str]] = None,
        enable: bool = True,
        logger: Logger = None
    ):
        super().__init__()
        self.logger = Logger(class_name=self.__class__.__name__)
        self.enable = enable
        self.proxies = proxies or []
        self.proxy_pool = cycle(self.proxies) if self.proxies else None

        self.logger.info(
            f"Initialized with {len(self.proxies)} proxies. Enabled: {self.enable}"
        )

    def process_request(self, url: str, kwargs: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
        if self.enable and self.proxy_pool:
            proxy = next(self.proxy_pool)
            kwargs["proxies"] = {"http": proxy, "https": proxy}
            self.logger.debug(f"Using proxy: {proxy}")
        else:
            self.logger.debug("Proxy disabled or no proxies available.")
        return url, kwargs

    def process_response(self, response: Optional[Response], **kwargs: Any) -> Optional[Response]:
        return response

    def update_proxies(self, new_proxies: List[str]) -> None:
        self.proxies = new_proxies
        self.proxy_pool = cycle(self.proxies) if self.proxies else None
        self.logger.info(f"Proxies updated. Total proxies: {len(self.proxies)}")

    def enable_proxies(self) -> None:
        self.enable = True
        self.logger.info("Proxy usage enabled.")

    def disable_proxies(self) -> None:
        self.enable = False
        self.logger.info("Proxy usage disabled.")