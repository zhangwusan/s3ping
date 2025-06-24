import os
import sys

# Add src/ to path for module resolution
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.s3ping.registry import build_pipeline
from src.s3ping.utils.load import load_config


if __name__ == "__main__":
    config = load_config("./src/s3ping/config/scrapes/default.yaml")
    pipeline = build_pipeline(config)
    pipeline.run()