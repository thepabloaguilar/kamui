from enum import Enum
from typing import Dict, Any

import httpx
import orjson
from returns.result import Result, Success, Failure
from httpx import HTTPError, Response

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
    def __make_request(
        self,
        method: HttpMethod,
        url: str,
        payload: Dict[str, Any] = None,
        headers: Dict[str, str] = None,
        timeout: int = 5.0,
    ) -> Result[JsonResponse, str]:
        _data = orjson.dumps(payload) if payload else None
        try:
            response = httpx.request(
                method=method.value,
                url=url,
                data=_data,
                headers=headers,
                timeout=timeout,
            )
            return self.__validate_response(response)
        except HTTPError as ex:
            return Failure(f"{ex.__class__.__name__} calling {ex.request.url}")

    def __validate_response(self, response: Response) -> Result[JsonResponse, str]:
        http_status = HttpStatus(response.status_code)
        if http_status in [HttpStatus.OK, HttpStatus.CREATED]:
            return Success(response.json())
        return Failure(http_status.name)

    def get(
        self, url: str, headers: Dict[str, str] = None, timeout: int = 5.0,
    ) -> Result[JsonResponse, str]:
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
    ) -> Result[JsonResponse, str]:
        response = self.__make_request(
            method=HttpMethod.POST,
            payload=payload,
            url=url,
            headers=headers,
            timeout=timeout,
        )
        return response


client = HttpClient()
