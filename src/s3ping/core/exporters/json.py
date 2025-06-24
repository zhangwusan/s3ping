import json
from typing import Any
from src.s3ping.constants.file_mode import FileMode
from src.s3ping.core.exporters.base import BaseExporter


class JsonExporter(BaseExporter):
    EXPECTED_EXTENSION = ".json"

    def export(self, data: Any, mode: FileMode = FileMode.WRITE) -> None:
        with open(self.output_path, mode.value, encoding="utf-8") as f:
            if mode == FileMode.WRITE:
                json.dump(data, f, ensure_ascii=False, indent=2)
            elif mode == FileMode.APPEND:
                if isinstance(data, list):
                    for item in data:
                        f.write(json.dumps(item, ensure_ascii=False) + "\n")
                else:
                    f.write(json.dumps(data, ensure_ascii=False) + "\n")
    