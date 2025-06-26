import os
from datetime import datetime
from abc import ABC, abstractmethod
from typing import Any, Optional

from src.s3ping.loggers.logger import Logger

class BaseExporter(ABC):
    DEFAULT_OUTPUT_DIR = "./output"
    EXPECTED_EXTENSION = ".txt"

    def __init__(self, output_path: Optional[str] = None, logger: Optional[Logger] = None):
        self.logger = logger or Logger(class_name=self.__class__.__name__)

        if output_path is None:
            output_path = self._generate_default_filename()
        self.output_path = output_path
        self._ensure_output_path()
    

    def _generate_default_filename(self) -> str:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"export_{timestamp}{self.EXPECTED_EXTENSION}"
        return os.path.join(self.DEFAULT_OUTPUT_DIR, filename)

    def _ensure_output_path(self):
        dir_path = os.path.dirname(self.output_path)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)

    @abstractmethod
    def export(self, data: Any) -> None:
        pass