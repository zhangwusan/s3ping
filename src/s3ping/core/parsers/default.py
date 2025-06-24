from src.s3ping.core.parsers.base import BaseParser
import json

class DefaultParser(BaseParser):
    def __init__(self, response):
        super().__init__(response)
        
    def parse(self) -> dict:
        """Extract common useful page information."""
        return {
            "title": self.get_title(),
            "meta": self.get_meta_tags(),
            "open_graph": self.get_open_graph_tags(),
            "twitter_cards": self.get_twitter_cards(),
            "headings": self.get_headings(),
            "links": self.get_links(),
            "images": self.get_images(),
            "tables": self.get_tables(),
            "json_ld": self.get_json_ld(),
            "canonical_url": self.get_canonical_url(),
            "charset": self.get_charset(),
            "language": self.get_language(),
            "forms": self.get_forms(),
        }

    def get_title(self) -> str:
        return self.soup.title.string.strip() if self.soup.title else ""

    def get_meta_tags(self) -> dict:
        metas = {}
        for tag in self.soup.find_all("meta"):
            if tag.get("name") and tag.get("content"):
                metas[tag["name"].lower()] = tag["content"].strip()
            elif tag.get("http-equiv") and tag.get("content"):
                metas[tag["http-equiv"].lower()] = tag["content"].strip()
        return metas

    def get_open_graph_tags(self) -> dict:
        og = {}
        for tag in self.soup.find_all("meta", property=lambda x: x and x.startswith("og:")):
            og[tag["property"]] = tag.get("content", "").strip()
        return og

    def get_twitter_cards(self) -> dict:
        twitter = {}
        for tag in self.soup.find_all("meta", attrs={"name": lambda x: x and x.startswith("twitter:")}):
            twitter[tag["name"]] = tag.get("content", "").strip()
        return twitter

    def get_headings(self) -> dict:
        return {
            f"h{i}": [h.get_text(strip=True) for h in self.soup.find_all(f"h{i}")]
            for i in range(1, 7)
        }

    def get_links(self) -> list:
        return [a["href"].strip() for a in self.soup.find_all("a", href=True)]

    def get_images(self) -> list:
        return [{"src": img.get("src", ""), "alt": img.get("alt", "")} for img in self.soup.find_all("img")]

    def get_tables(self) -> list:
        tables = []
        for table in self.soup.find_all("table"):
            rows = []
            for tr in table.find_all("tr"):
                cells = [td.get_text(strip=True) for td in tr.find_all(["td", "th"])]
                rows.append(cells)
            tables.append(rows)
        return tables

    def get_json_ld(self) -> list:
        data = []
        for script in self.soup.find_all("script", type="application/ld+json"):
            try:
                parsed = json.loads(script.string)
                data.append(parsed)
            except Exception:
                continue
        return data

    def get_canonical_url(self) -> str:
        link = self.soup.find("link", rel="canonical")
        return link["href"].strip() if link and link.has_attr("href") else ""

    def get_charset(self) -> str:
        tag = self.soup.find("meta", charset=True)
        if tag:
            return tag["charset"].strip()
        # fallback to http-equiv charset
        tag = self.soup.find("meta", attrs={"http-equiv": "Content-Type"})
        if tag and tag.has_attr("content"):
            content = tag["content"]
            if "charset=" in content:
                return content.split("charset=")[-1].strip()
        return ""

    def get_language(self) -> str:
        html_tag = self.soup.find("html")
        if html_tag and html_tag.has_attr("lang"):
            return html_tag["lang"].strip()
        return ""

    def get_forms(self) -> list:
        forms = []
        for form in self.soup.find_all("form"):
            inputs = []
            for inp in form.find_all(["input", "textarea", "select"]):
                input_info = {
                    "type": inp.get("type", "text"),
                    "name": inp.get("name"),
                    "value": inp.get("value"),
                    "placeholder": inp.get("placeholder"),
                }
                inputs.append(input_info)
            forms.append({
                "action": form.get("action"),
                "method": form.get("method", "GET").upper(),
                "inputs": inputs,
            })
        return forms