import json
import os
from typing import Any

from s3ping.core.exporter.base import BaseExporter


class JsonExporter(BaseExporter):
    def __init__(self, filepath: str = "output.json", mode: str = "overwrite"):
        """
        mode:
          - "overwrite": overwrite entire file (default)
          - "append": append data as list items to existing JSON list in file
          - "stream": write one JSON object per line (JSON Lines format)
        """
        self.filepath = filepath
        self.mode = mode.lower()
        dirpath = os.path.dirname(os.path.abspath(self.filepath))
        os.makedirs(dirpath, exist_ok=True)

        # Validate mode
        if self.mode not in {"overwrite", "append", "stream"}:
            raise ValueError(f"Unsupported mode: {self.mode}")

    def export(self, data: Any) -> None:
        if self.mode == "overwrite":
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

        elif self.mode == "append":
            existing = []
            if os.path.isfile(self.filepath):
                try:
                    with open(self.filepath, "r", encoding="utf-8") as f:
                        existing = json.load(f)
                except Exception:
                    existing = []

            # If existing is not a list, overwrite
            if not isinstance(existing, list):
                existing = []

            if isinstance(data, list):
                existing.extend(data)
            else:
                existing.append(data)

            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(existing, f, ensure_ascii=False, indent=2)

        elif self.mode == "stream":
            # Write JSON object per line
            with open(self.filepath, "a", encoding="utf-8") as f:
                if isinstance(data, list):
                    for item in data:
                        f.write(json.dumps(item, ensure_ascii=False) + "\n")
                else:
                    f.write(json.dumps(data, ensure_ascii=False) + "\n")