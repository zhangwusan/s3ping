from typing import Any, Dict, Optional, Tuple
import time

from requests.models import Response
from s3ping.core.utils.logger import Logger
from s3ping.middlewares.base import BaseMiddleware
from s3ping.solvers.base import CaptchaSolver


class CaptchaMiddleware(BaseMiddleware):
    def __init__(self, auto_solve: bool = False, solver: Optional[CaptchaSolver] = None, logger: Logger = None):
        """
        Middleware to detect and optionally solve CAPTCHA pages in responses.

        Args:
            auto_solve (bool): Whether to attempt CAPTCHA solving (simulated).
        """
        super().__init__()
        self.logger = Logger(class_name=self.__class__.__name__)
        self.auto_solve = auto_solve
        self.solver = solver

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

        if "captcha" in html.lower() or "g-recaptcha" in html.lower() or "cf-chl-bypass" in html.lower():
            self.logger.warning(f"CAPTCHA detected on {url}")

            if not self.auto_solve:
                self.logger.warning("CAPTCHA auto-solve is disabled. Returning None.")
                return None
            
            if self.solver:
                self.logger.info("Solving CAPTCHA using solver...")
                if self.solve_captcha(url, html):
                    self.logger.info("CAPTCHA solved.")
                    return None  # Let HttpClient retry if needed
                else:
                    self.logger.warning("CAPTCHA solving failed.")
                    return None
            else:
                self.logger.warning("No solver provided.")
                return None

        return response

    def solve_captcha(self, url: str, html: str) -> bool: 
        """Calls external solver and injects token if needed."""
        if not self.solver:
            self.logger.error("No solver attached.")
            return False
        
        try:
            site_key = self.extract_site_key(html)
            if not site_key:
                self.logger.error("Site key not found.")
                return False

            token = self.solver.solve(site_key=site_key, url=url)
            if token:
                self.logger.info(f"Received token: {token[:30]}...")
                return True
            else:
                self.logger.warning("Solver returned no token.")
                return False
        except Exception as e:
            self.logger.error(f"Error solving CAPTCHA: {e}")
            return False
    
    def extract_site_key(self, html: str) -> Optional[str]:
        import re
        match = re.search(r'data-sitekey="([a-zA-Z0-9-_]+)"', html)
        return match.group(1) if match else None