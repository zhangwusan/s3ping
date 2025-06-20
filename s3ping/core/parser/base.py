from typing import Any


class BaseParser:
    def parse(self, content: str) -> Any:
        raise NotImplementedError