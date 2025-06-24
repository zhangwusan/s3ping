from typing import Any


class BaseParser:
    def parse(self, content: str, parser: str = "lxml") -> Any:
        raise NotImplementedError