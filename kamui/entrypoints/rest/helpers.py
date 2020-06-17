from functools import wraps
from typing import Callable, Tuple, Any, TypeVar

import orjson
from flask import Response, request
from pydantic import ValidationError
from returns.result import Result, Success, Failure

from kamui.core.use_case.failure import NewFailureDetails

_SuccessType = TypeVar("_SuccessType")
_FailureType = TypeVar("_FailureType")


def json_response(function: Callable[..., Tuple[Any, int]]) -> Callable[..., Response]:
    @wraps(function)
    def decorator(*args: Any, **kwargs: Any) -> Response:
        return_, status_code = function(*args, **kwargs)
        if isinstance(return_, Response):
            return return_
        return _create_response(return_, status_code)

    return decorator


def parse_request_body(
    clazz: Any,
) -> Callable[
    [Callable[..., Result[_SuccessType, _FailureType]]],
    Callable[..., Result[_SuccessType, _FailureType]],
]:
    def _parse_request_body(
        function: Callable[..., Result[_SuccessType, _FailureType]]
    ) -> Callable[..., Result[_SuccessType, _FailureType]]:
        @wraps(function)
        def decorator(*args: Any, **kwargs: Any) -> Result[_SuccessType, _FailureType]:
            try:
                json_body = orjson.loads(request.data)
                request_body = Success(clazz(**json_body))
            except (ValidationError, TypeError) as error:
                raw_errors = getattr(error, "raw_errors", [])
                errors = {e._loc: e.exc.msg_template for e in raw_errors}
                failure = NewFailureDetails(
                    reason="BODY_PARSE_ERROR",
                    failure_message="Body request has to match exactly as the body schema",  # noqa: E501
                    attributes={
                        "expected_body_schema": clazz.__pydantic_model__.schema(),
                        "field_errors": errors,
                    },
                )
                request_body = Failure(_create_response(failure, 400))
            return function(*args, **kwargs, request_body=request_body)

        return decorator

    return _parse_request_body


def unwrap_result_response(
    success_status_code: int,
) -> Callable[
    [Callable[..., Result[_SuccessType, _FailureType]]], Callable[..., Tuple[Any, int]]
]:
    def _unwrap_result_response(
        function: Callable[..., Result[_SuccessType, _FailureType]]
    ) -> Callable[..., Tuple[Any, int]]:
        @wraps(function)
        def decorator(*args: Any, **kwargs: Any) -> Tuple[Any, int]:
            # TODO: Improve failure treatment
            return (
                function(*args, **kwargs)
                .map(lambda response: (response, success_status_code))
                .fix(lambda failure: (failure, 503))
                .unwrap()
            )

        return decorator

    return _unwrap_result_response


def _create_response(response_body: Any, status_code: int) -> Response:
    return Response(
        response=orjson.dumps(response_body),
        status=status_code,
        mimetype="application/json",
    )
