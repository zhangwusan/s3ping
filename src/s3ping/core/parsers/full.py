from typing import List, Dict, Any
from bs4 import Tag
from src.s3ping.core.parsers.base import BaseParser
from src.s3ping.responses.html import HTMLResponse

class FullDOMParser(BaseParser):
    def parse(self) -> List[Dict[str, Any]]:
        return self._parse_element(self.soup, path=[])

    def _parse_element(self, element: Tag, path: List[str]) -> List[Dict[str, Any]]:
        parsed = []

        for i, child in enumerate(element.children):
            if isinstance(child, Tag):
                # Build current node's selector
                tag_name = child.name
                tag_id = f"#{child['id']}" if 'id' in child.attrs else ""
                tag_classes = "." + ".".join(child.get("class", [])) if "class" in child.attrs else ""
                selector = f"{tag_name}{tag_id}{tag_classes}"

                # Construct full path
                full_path = path + [selector]
                location = " > ".join(full_path)

                # Store node info
                node_info = {
                    "tag": tag_name,
                    "attrs": dict(child.attrs),
                    "text": child.get_text(strip=True),
                    "location": location
                }
                parsed.append(node_info)

                # Recursively parse children
                parsed.extend(self._parse_element(child, full_path))

        return parsed