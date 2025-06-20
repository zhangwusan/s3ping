from s3ping.core.parser.base import BaseParser
from s3ping.core.parser.html import HtmlParser

class DefaultParser(BaseParser):
    def parse(self, content: str):
        parser = HtmlParser(content)

        title_tag = parser.find_element("title")
        title_text = parser.extract_text(title_tag)

        return {
            "title": title_text
        }