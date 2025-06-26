from typing import Any, List, Union
from src.s3ping.constants.file_mode import FileMode
from src.s3ping.core.exporters.base import BaseExporter


class HtmlExporter(BaseExporter):
    EXPECTED_EXTENSION = ".html"

    def export(self, data: Union[str, bytes, List[Union[str, bytes]]], mode: FileMode = FileMode.WRITE):
        if not data:
            self.logger and self.logger.warning("No data to export", caller=self)
            return

        # Normalize to list
        if isinstance(data, (str, bytes)):
            data = [data]

        html_blocks = []
        for item in data:
            if isinstance(item, bytes):
                item = item.decode("utf-8", errors="replace")
            html_blocks.append(item.strip())

        with open(self.output_path, mode.value, encoding="utf-8") as f:
            for block in html_blocks:
                f.write(block)
                f.write("\n\n") 