from enum import Enum, auto

class EngineType(Enum):
    REQUESTS = auto()
    CLOUDSCRAPER = auto()
    PLAYWRIGHT = auto()
    SELENIUM = auto()