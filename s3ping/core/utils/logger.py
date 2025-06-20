import logging
import os
from datetime import datetime
import colorlog
from typing import Optional, List


class Logger:
    def __init__(
        self,
        log_paths: Optional[List[str]] = None,  # If None or empty, no file logging
        log_level_file: int = logging.DEBUG,
        log_level_console: int = logging.DEBUG,
        log_format: str = "%(asctime)s - %(levelname)s - %(message)s",
        date_format: str = "%Y-%m-%d %H:%M:%S",
        class_name: Optional[str] = None,
        enable_logging: bool = True,
    ):
        if not enable_logging:
            self.logger = None
            return

        self.class_name = class_name
        self.logger = logging.getLogger(f"Logger_{id(self)}")
        self.logger.propagate = False

        if self.logger.hasHandlers():
            return

        self.logger.setLevel(logging.DEBUG)

        # Add file handlers only if log_paths is provided and non-empty
        if log_paths:
            file_formatter = logging.Formatter(log_format, datefmt=date_format)
            for path in log_paths:
                os.makedirs(os.path.dirname(path), exist_ok=True)
                file_handler = logging.FileHandler(path)
                file_handler.setLevel(log_level_file)
                file_handler.setFormatter(file_formatter)
                self.logger.addHandler(file_handler)

        # Always add console handler with color
        console_formatter = colorlog.ColoredFormatter(
            "%(log_color)s" + log_format,
            datefmt=date_format,
            log_colors={
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold_red",
            },
        )
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level_console)
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

    def _format_msg(self, msg: str, caller: Optional[object]) -> str:
        if self.class_name:
            return f"[{self.class_name}] {msg}"
        elif caller:
            return f"[{caller.__class__.__name__}] {msg}"
        return msg

    def debug(self, msg: str, *args, caller: Optional[object] = None, **kwargs):
        if self.logger:
            self.logger.debug(self._format_msg(msg, caller), *args, **kwargs)

    def info(self, msg: str, *args, caller: Optional[object] = None, **kwargs):
        if self.logger:
            self.logger.info(self._format_msg(msg, caller), *args, **kwargs)

    def warning(self, msg: str, *args, caller: Optional[object] = None, **kwargs):
        if self.logger:
            self.logger.warning(self._format_msg(msg, caller), *args, **kwargs)

    def error(self, msg: str, *args, caller: Optional[object] = None, **kwargs):
        if self.logger:
            self.logger.error(self._format_msg(msg, caller), *args, **kwargs)

    def critical(self, msg: str, *args, caller: Optional[object] = None, **kwargs):
        if self.logger:
            self.logger.critical(self._format_msg(msg, caller), *args, **kwargs)