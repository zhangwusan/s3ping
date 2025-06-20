from typing import Any, Dict, Optional, Tuple
import time

from requests.models import Response
from s3ping.s3ping.core.utils.logger import Logger
from s3ping.middlewares.base import BaseMiddleware


class CaptchaMiddleware(BaseMiddleware):
    def __init__(self, auto_solve: bool = False, logger: Logger = None):
        """
        Middleware to detect and optionally solve CAPTCHA pages in responses.

        Args:
            auto_solve (bool): Whether to attempt CAPTCHA solving (simulated).
        """
        super().__init__()
        self.logger = Logger(class_name=self.__class__.__name__)
        self.auto_solve = auto_solve

        self.logger.info(f"Initialized | Auto-solve: {self.auto_solve}")

    def process_request(self, url: str, kwargs: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
        # No modifications to request
        return url, kwargs

    def process_response(self, response: Optional[Response]) -> Optional[Response]:
        if response is None or not hasattr(response, "text"):
            self.logger.warning("Received empty or invalid response object.")
            return response

        html = response.text
        url = getattr(response, "url", "unknown URL")

        if "captcha" in html.lower() or "g-recaptcha" in html.lower():
            self.logger.warning(f"CAPTCHA detected on {url}")

            if not self.auto_solve:
                self.logger.warning("CAPTCHA auto-solve is disabled. Returning None.")
                return None

            self.logger.info("Attempting to solve CAPTCHA... (simulated)")
            time.sleep(5)
            return None

        return response