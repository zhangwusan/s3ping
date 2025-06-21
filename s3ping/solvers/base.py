from abc import ABC, abstractmethod
from typing import Optional

class CaptchaSolver(ABC):
    @abstractmethod
    def solve(self, site_key: str, url: str) -> Optional[str]:
        """Solves CAPTCHA and returns the token if successful"""
        pass