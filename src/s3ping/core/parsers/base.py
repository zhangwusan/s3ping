from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from src.s3ping.responses.html import HTMLResponse

class BaseParser(ABC):
    def __init__(self, response: HTMLResponse):
        self.response = response
        self.soup = BeautifulSoup(response.content, "html.parser")

    @abstractmethod
    def parse(self):
        """Should return a list of extracted data dictionaries"""
        pass