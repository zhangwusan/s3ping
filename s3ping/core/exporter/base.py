from typing import Any


class BaseExporter:
    def export(self, data: Any) -> None:
        raise NotImplementedError