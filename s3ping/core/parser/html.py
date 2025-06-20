import re
from bs4 import BeautifulSoup, Tag
from typing import Optional, List, Union, Callable, Dict

class HtmlParser:
    def __init__(self, html: str, parser: str = "lxml"):
        self.soup: BeautifulSoup = BeautifulSoup(html, parser)

    def extract_text(self, element: Optional[Tag], strip: bool = True) -> str:
        return element.get_text(strip=strip) if element else ""

    def extract_attribute(self, element: Optional[Tag], attr: str) -> Optional[str]:
        return element[attr] if element and element.has_attr(attr) else None

    def find_element(self, selector: str) -> Optional[Tag]:
        return self.soup.select_one(selector)

    def find_all_elements(self, selector: str) -> List[Tag]:
        return self.soup.select(selector)

    def get_first_text(self, selector: str, filter_fn: Optional[Callable[[Tag], bool]] = None) -> Optional[str]:
        element = self.find_element(selector)
        return self.extract_text(element) if element and (not filter_fn or filter_fn(element)) else None

    def get_first_attr(self, selector: str, attr: str, filter_fn: Optional[Callable[[Tag], bool]] = None) -> Optional[str]:
        element = self.find_element(selector)
        return self.extract_attribute(element, attr) if element and (not filter_fn or filter_fn(element)) else None

    def get_all_texts(self, selector: str, filter_fn: Optional[Callable[[Tag], bool]] = None) -> List[str]:
        elements = self.find_all_elements(selector)
        return [self.extract_text(el) for el in (filter(filter_fn, elements) if filter_fn else elements)]

    def get_all_attrs(self, selector: str, attr: str, filter_fn: Optional[Callable[[Tag], bool]] = None) -> List[str]:
        elements = self.find_all_elements(selector)
        return [self.extract_attribute(el, attr) for el in (filter(filter_fn, elements) if filter_fn else elements) if self.extract_attribute(el, attr)]
    

class HtmlFlexibleParser(HtmlParser):
    def find_elements_by_class_regex(self, tag: str, class_pattern: str) -> List[Tag]:
        regex = re.compile(class_pattern)
        return self.soup.find_all(tag, class_=regex)

    def find_elements_fuzzy(
        self,
        tag: Optional[str] = None,
        attrs: Optional[dict] = None,
        text_contains: Optional[str] = None,
        class_pattern: Optional[str] = None
    ) -> List[Tag]:
        def match(tag_obj: Tag) -> bool:
            if class_pattern:
                if not tag_obj.has_attr('class') or not any(re.search(class_pattern, c) for c in tag_obj['class']):
                    return False
            if text_contains and text_contains not in tag_obj.get_text():
                return False
            if attrs:
                for k, v in attrs.items():
                    if tag_obj.get(k) != v:
                        return False
            return True

        return self.soup.find_all(tag if tag else True, match)

    def find_by_text_keywords(self, keywords: List[str], tag: str = "a") -> List[Tag]:
        return [el for el in self.soup.find_all(tag) if any(k in el.get_text() for k in keywords)]

    def extract_links_by_keywords(self, keywords: List[str], tag: str = "a") -> List[Dict[str, str]]:
        links = self.find_by_text_keywords(keywords, tag)
        return [
            {
                "text": self.extract_text(link),
                "href": self.extract_attribute(link, "href") or ""
            }
            for link in links
        ]