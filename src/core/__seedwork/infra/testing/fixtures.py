from typing import Any, Optional
from dataclasses import dataclass


@dataclass
class Request:
    body: Any


@dataclass
class Response:
    body: Any


@dataclass
class HttpExpect:
    request: Request
    response: Optional[Response] = None
    exception: Optional[Exception] = None

@dataclass
class SearchExpect:
    send_data: dict
    expected: 'SearchExpect.Expected'
    entities: list
    
    @dataclass
    class Expected:
        entities: list
        meta: dict