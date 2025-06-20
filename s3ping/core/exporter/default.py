import json
import os
from typing import Any

from s3ping.core.exporter.base import BaseExporter


class JsonExporter(BaseExporter):
    def __init__(self, filepath: str = "output.json"):
        self.filepath = filepath
        dirpath = os.path.dirname(os.path.abspath(self.filepath))
        os.makedirs(dirpath, exist_ok=True)

    def export(self, data: Any) -> None:
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)