from typing import Any
from django.http.request import HttpRequest
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

def make_request(http_method: str, url: str = '/', send_data: Any = None) -> Request:
    _request_factory = APIRequestFactory()
    http_method_func = getattr(_request_factory, http_method)
    http_request: HttpRequest = http_method_func(url)
    request = Request(http_request)
    request._full_data = send_data
    return request