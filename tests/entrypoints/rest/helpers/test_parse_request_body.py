import orjson
from flask import Response, Flask
from pydantic.dataclasses import dataclass
from returns.result import Result

from kamui.entrypoints.rest.helpers import parse_request_body


@dataclass
class User:
    name: str
    age: int


def test_should_return_success_when_request_body_match_with_expected_class(
    flask_app: Flask,
) -> None:
    with flask_app.test_request_context(data='{"name": "TEST", "age": 22}'):

        @parse_request_body(User)
        def func(request_body: Result[User, Response]) -> Result[User, Response]:
            return request_body

        actual = func()
    assert isinstance(actual, Result.success_type)
    assert actual.unwrap() == User("TEST", 22)


def test_should_return_failure_when_request_body_has_a_missing_field(
    flask_app: Flask,
) -> None:
    with flask_app.test_request_context(data='{"name": "TEST"}'):

        @parse_request_body(User)
        def func(request_body: Result[User, Response]) -> Result[User, Response]:
            return request_body

        actual = func()
    assert isinstance(actual, Result.failure_type)
    json_response = orjson.loads(actual.failure().response[0])
    assert json_response["reason"] == "BODY_PARSE_ERROR"


def test_should_return_failure_when_request_body_has_field_with_wrong_type(
    flask_app: Flask,
) -> None:
    expected_field_errors = {"age": "value is not a valid integer"}
    with flask_app.test_request_context(data='{"name": "TEST", "age": "STRING"}'):

        @parse_request_body(User)
        def func(request_body: Result[User, Response]) -> Result[User, Response]:
            return request_body

        actual = func()
    assert isinstance(actual, Result.failure_type)
    json_response = orjson.loads(actual.failure().response[0])
    assert "BODY_PARSE_ERROR" == json_response["reason"]
    assert expected_field_errors == json_response["attributes"]["field_errors"]
