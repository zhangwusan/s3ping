class HTMLResponse:
    def __init__(self, content: str, url: str, status_code: int = 200):
        self.content = content.encode("utf-8")
        self.text = content
        self.url = url
        self.status_code = status_code

    def json(self):
        raise NotImplementedError("HTMLResponse does not support .json()")