from enum import Enum
from typing import Dict, Any

import httpx
import orjson
from returns.result import Result, Success, Failure
from httpx import HTTPError, Response

from kamui.core.usecase.failure import DataProviderFailureDetails

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
    ) -> Result[JsonResponse, DataProviderFailureDetails]:
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
            return Failure(
                DataProviderFailureDetails(
                    dataprovider_type="REST",
                    reason=ex.__class__.__name__,
                    attributes={"origin": "EXCEPTION", "url": ex.request.url},
                )
            )

    def __validate_response(
        self, response: Response
    ) -> Result[JsonResponse, DataProviderFailureDetails]:
        http_status = HttpStatus(response.status_code)
        if http_status in [HttpStatus.OK, HttpStatus.CREATED]:
            return Success(response.json())
        return Failure(
            DataProviderFailureDetails(
                dataprovider_type="REST",
                reason=http_status.name,
                attributes={
                    "origin": "HTTP_STATUS",
                    "http_status_code": http_status.value,
                    "response": response.json(),
                },
            )
        )

    def get(
        self, url: str, headers: Dict[str, str] = None, timeout: int = 5.0,
    ) -> Result[JsonResponse, DataProviderFailureDetails]:
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
    ) -> Result[JsonResponse, DataProviderFailureDetails]:
        response = self.__make_request(
            method=HttpMethod.POST,
            payload=payload,
            url=url,
            headers=headers,
            timeout=timeout,
        )
        return response


client = HttpClient()
