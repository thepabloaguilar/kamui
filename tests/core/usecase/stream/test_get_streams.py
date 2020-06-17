from unittest.mock import Mock
from uuid import uuid4

import pytest
from returns.result import Failure, Result, Success

from kamui.core.entity.source import SourceType
from kamui.core.entity.stream import Stream
from kamui.core.use_case.failure import FailureDetails, BusinessFailureDetails
from kamui.core.use_case.stream.get_streams import FindStreams, GetStreamsUseCase


@pytest.fixture(scope="function")
def find_streams() -> Mock:
    return Mock(spec=FindStreams)


@pytest.fixture(scope="function")
def get_streams_usecase(find_streams: Mock) -> GetStreamsUseCase:
    return GetStreamsUseCase(find_streams)


def test_should_return_streams_correctly(
    get_streams_usecase: GetStreamsUseCase, find_streams: Mock
) -> None:
    streams_list = [
        Stream(
            stream_id=uuid4(),
            name="STREAM_ONE",
            source_type=SourceType.TOPIC,
            source_name="some_topic",
        ),
        Stream(
            stream_id=uuid4(),
            name="STREAM_TWO",
            source_type=SourceType.STREAM,
            source_name="STREAM_ONE",
        ),
    ]
    find_streams.return_value = Success(streams_list)

    actual = get_streams_usecase()

    find_streams.assert_called_once()
    assert isinstance(actual, Result.success_type)
    assert isinstance(actual.unwrap(), list)
    assert streams_list == actual.unwrap()


def test_should_return_failure_when_find_streams_fails(
    get_streams_usecase: GetStreamsUseCase, find_streams: Mock
) -> None:
    failure = FailureDetails(reason="TEST_FIND_STREAMS_FAIL")
    find_streams.return_value = Failure(failure)

    actual = get_streams_usecase()

    find_streams.assert_called_once()
    assert isinstance(actual, Result.failure_type)
    assert isinstance(actual.failure(), BusinessFailureDetails)
    assert "NON_BUSINESS_RULE_CAUSE" == actual.failure().reason
    assert failure == actual.failure().failure_due
