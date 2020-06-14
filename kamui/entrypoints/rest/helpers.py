from functools import wraps
from typing import Callable, Tuple, Any, TypeVar

import orjson
from flask import Response
from returns.result import Result

_SuccessType = TypeVar("_SuccessType")
_FailureType = TypeVar("_FailureType")


def json_response(function: Callable[..., Tuple[Any, int]]) -> Callable[..., Response]:
    @wraps(function)
    def decorator(*args: Any, **kwargs: Any) -> Response:
        return_, status_code = function(*args, **kwargs)
        return Response(
            response=orjson.dumps(return_),
            status=status_code,
            mimetype="application/json",
        )

    return decorator


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
