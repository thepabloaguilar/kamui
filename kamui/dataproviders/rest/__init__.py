from enum import Enum
from typing import Dict, Any

import httpx
import orjson


JsonResponse = Dict[str, Any]


class HttpMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    OPTIONS = "OPTIONS"


class HttpStatus(Enum):
    CONTINUE = 100
    OK = 200
    CREATED = 201
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    REQUEST_TIMEOUT = 408
    PRECONDITION_FAILED = 412
    INTERNAL_SERVER_ERROR = 500
    BAD_GATEWAY = 502
    SERVICE_UNAVAILABLE = 503
    GATEWAY_TIMEOUT = 504


class HttpClient:
    # TODO: Make exception treatment
    def __make_request(
        self,
        method: HttpMethod,
        url: str,
        payload: Dict[str, Any] = None,
        headers: Dict[str, str] = None,
        timeout: int = 5.0,
    ) -> JsonResponse:
        _data = orjson.dumps(payload) if payload else None
        return httpx.request(
            method=method.value, url=url, data=_data, headers=headers, timeout=timeout
        ).json()

    def get(
        self, url: str, headers: Dict[str, str] = None, timeout: int = 5.0,
    ) -> JsonResponse:
        response = self.__make_request(
            method=HttpMethod.GET, url=url, headers=headers, timeout=timeout
        )
        return response

    def post(
        self,
        url: str,
        payload: Dict[str, str],
        headers: Dict[str, str] = None,
        timeout: int = 5.0,
    ) -> JsonResponse:
        response = self.__make_request(
            method=HttpMethod.POST,
            payload=payload,
            url=url,
            headers=headers,
            timeout=timeout,
        )
        return response


client = HttpClient()
