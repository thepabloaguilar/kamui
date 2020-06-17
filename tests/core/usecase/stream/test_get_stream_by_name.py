from unittest.mock import Mock

import pytest
from returns.result import Failure, Result, Success

from kamui.core.entity.stream import KSQLStreamDetailed
from kamui.core.use_case.failure import FailureDetails, BusinessFailureDetails
from kamui.core.use_case.stream.get_stream_by_name import (
    GetStreamByName,
    GetStreamByNameUseCase,
)


@pytest.fixture(scope="function")
def get_stream_by_name() -> Mock:
    return Mock(spec=GetStreamByName)


@pytest.fixture(scope="function")
def get_stream_by_name_usecase(get_stream_by_name: Mock) -> GetStreamByNameUseCase:
    return GetStreamByNameUseCase(get_stream_by_name)


def test_should_return_ksql_stream_detailed_correctly(
    get_stream_by_name_usecase: GetStreamByNameUseCase, get_stream_by_name: Mock
) -> None:
    ksql_stream_detailed = KSQLStreamDetailed(
        name="SUCCESS_TEST_STREAM",
        fields=[],
        type="STREAM",
        format="AVRO",
        topic="topic",
    )
    get_stream_by_name.return_value = Success(ksql_stream_detailed)

    actual = get_stream_by_name_usecase("SUCCESS_TEST_STREAM")

    get_stream_by_name.assert_called_once()
    get_stream_by_name.assert_called_with("SUCCESS_TEST_STREAM")
    assert isinstance(actual, Result.success_type)
    assert isinstance(actual.unwrap(), KSQLStreamDetailed)
    assert ksql_stream_detailed == actual.unwrap()


def test_should_return_failure_when_an_error_occurred_while_getting_stream_names(
    get_stream_by_name_usecase: GetStreamByNameUseCase, get_stream_by_name: Mock
) -> None:
    failure = Failure(FailureDetails(reason="FAILURE_TEST"))
    get_stream_by_name.return_value = failure

    actual = get_stream_by_name_usecase("MY_STREAM_NAME")

    get_stream_by_name.assert_called_once()
    get_stream_by_name.assert_called_with("MY_STREAM_NAME")
    assert isinstance(actual, Result.failure_type)
    assert isinstance(actual.failure(), BusinessFailureDetails)
    assert "NON_BUSINESS_RULE_CAUSE" == actual.failure().reason
    assert failure.failure() == actual.failure().failure_due
