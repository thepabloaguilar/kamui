import orjson
from flask import Response
from pydantic.dataclasses import dataclass

from kamui.entrypoints.rest.helpers import json_response


@dataclass
class Object:
    attribute_a: str
    attribute_b: int


def test_should_return_response_object_correctly() -> None:
    decorated_function = json_response(lambda obj, status_code: (obj, status_code))
    obj = Object("test_return_response_object_correctly", 1)

    actual = decorated_function(obj, 201)

    assert isinstance(actual, Response)
    assert orjson.dumps(obj) == actual.response[0]
    assert "application/json" == actual.mimetype
    assert 201 == actual.status_code


def test_should_ignore_status_code_when_decorated_function_returns_response_object() -> None:  # noqa: E501
    decorated_function = json_response(
        lambda obj, status_code: (
            Response(response=obj, status=100, mimetype="application/json"),
            status_code,
        )
    )
    obj = Object("test_ignore_status_code", 1)

    actual = decorated_function(obj, 201)

    assert isinstance(actual, Response)
    assert obj == actual.response
    assert "application/json" == actual.mimetype
    assert 100 == actual.status_code
