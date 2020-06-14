from functools import wraps
from typing import Callable, Tuple, Any

import orjson
from flask import Response


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
