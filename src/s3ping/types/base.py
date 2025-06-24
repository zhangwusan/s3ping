from typing import Dict, Any, Callable, Union
import requests
from src.s3ping.responses.html import HTMLResponse

RequestType = Dict[str, Any]
ResponseType = Union[requests.Response, HTMLResponse]
NextHandlerType = Callable[[RequestType], ResponseType]