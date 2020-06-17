from unittest.mock import Mock

import pytest
from returns.result import Failure, Result, Success

from kamui.core.entity.stream import KSQLStream
from kamui.core.use_case.failure import FailureDetails, BusinessFailureDetails
from kamui.core.use_case.stream.get_ksql_streams import (
    GetKSQLStreams,
    GetKSQLStreamsUseCase,
)


@pytest.fixture(scope="function")
def get_ksql_streams() -> Mock:
    return Mock(spec=GetKSQLStreams)


@pytest.fixture(scope="function")
def get_ksql_streams_use_case(get_ksql_streams: Mock) -> GetKSQLStreamsUseCase:
    return GetKSQLStreamsUseCase(get_ksql_streams)


def test_should_return_list_of_ksql_stream_correctly(
    get_ksql_streams_use_case: GetKSQLStreamsUseCase, get_ksql_streams: Mock
) -> None:
    ksql_streams_list = [
        KSQLStream("STREAM", "STREAM_ONE", "AVRO"),
        KSQLStream("STREAM", "STREAM_TWO", "JSON"),
        KSQLStream("STREAM", "STREAM_THREE", "AVRO"),
    ]
    get_ksql_streams.return_value = Success(ksql_streams_list)

    actual = get_ksql_streams_use_case()

    get_ksql_streams.assert_called_once()
    assert isinstance(actual, Result.success_type)
    assert isinstance(actual.unwrap(), list)
    assert ksql_streams_list == actual.unwrap()


def test_should_return_failure_when_an_error_occurred_while_getting_ksql_streams(
    get_ksql_streams_use_case: GetKSQLStreamsUseCase, get_ksql_streams: Mock
) -> None:
    failure = Failure(FailureDetails(reason="FAILURE_TEST"))
    get_ksql_streams.return_value = failure

    actual = get_ksql_streams_use_case()

    get_ksql_streams.assert_called_once()
    assert isinstance(actual, Result.failure_type)
    assert isinstance(actual.failure(), BusinessFailureDetails)
    assert "NON_BUSINESS_RULE_CAUSE" == actual.failure().reason
    assert failure.failure() == actual.failure().failure_due
