from unittest.mock import Mock
from uuid import uuid4

import pytest
from returns.result import Failure, Result, Success

from kamui.core.entity.stream import Stream
from kamui.core.usecase.failure import FailureDetails, BusinessFailureDetails
from kamui.core.usecase.stream.create_new_stream import (
    SaveStream,
    CreateNewStreamCommand,
    SourceType,
    CreateNewStreamFromStreamUsecase,
    CreateNewStreamFromStream,
)


@pytest.fixture(scope="function")
def create_new_stream_from_stream() -> Mock:
    return Mock(spec=CreateNewStreamFromStream)


@pytest.fixture(scope="function")
def save_stream() -> Mock:
    return Mock(spec=SaveStream)


@pytest.fixture(scope="function")
def create_new_stream_from_stream_usecase(
    create_new_stream_from_stream: Mock, save_stream: Mock
) -> CreateNewStreamFromStreamUsecase:
    return CreateNewStreamFromStreamUsecase(create_new_stream_from_stream, save_stream)


def test_should_return_stream_entity_correctly(
    create_new_stream_from_stream_usecase: CreateNewStreamFromStreamUsecase,
    create_new_stream_from_stream: Mock,
    save_stream: Mock,
) -> None:
    project_id = uuid4()
    command = CreateNewStreamCommand(
        project_id=project_id,
        stream_name="TEST_STREAM_SUCCESS",
        fields=[
            CreateNewStreamCommand.StreamField(name="field_one", type="BIGINT"),
            CreateNewStreamCommand.StreamField(name="field_two", type="STRING"),
            CreateNewStreamCommand.StreamField(name="field_three", type="INT"),
        ],
        source_name="TEST_STREAM",
        source_type=SourceType.STREAM,
    )
    stream = Stream(
        stream_id=uuid4(),
        name="TEST_STREAM_SUCCESS",
        source_type=SourceType.STREAM,
        source_name="TEST_STREAM",
    )
    create_new_stream_from_stream.return_value = Success(command)
    save_stream.return_value = Success(stream)

    actual = create_new_stream_from_stream_usecase(command)

    create_new_stream_from_stream.assert_called_with(command)
    save_stream.assert_called_with(command)
    assert isinstance(actual, Result.success_type)
    assert isinstance(actual.unwrap(), Stream)
    assert stream == actual.unwrap()


def test_should_return_failure_when_create_new_stream_from_stream_fails(
    create_new_stream_from_stream_usecase: CreateNewStreamFromStreamUsecase,
    create_new_stream_from_stream: Mock,
) -> None:
    command = CreateNewStreamCommand(
        project_id=uuid4(),
        stream_name="TEST_STREAM_FAILURE",
        fields=[CreateNewStreamCommand.StreamField(name="field_test", type="BIGINT")],
        source_name="TEST_STREAM",
        source_type=SourceType.STREAM,
    )
    failure = Failure(FailureDetails(reason="TEST_CREATE_NEW_STREAM_FROM_STREAM_FAILS"))
    create_new_stream_from_stream.return_value = failure

    actual = create_new_stream_from_stream_usecase(command)

    create_new_stream_from_stream.assert_called_with(command)
    assert isinstance(actual, Result.failure_type)
    assert isinstance(actual.failure(), BusinessFailureDetails)
    assert "NON_BUSINESS_RULE_CAUSE" == actual.failure().reason
    assert failure.failure() == actual.failure().failure_due


def test_should_return_failure_when_save_stream_fails(
    create_new_stream_from_stream_usecase: CreateNewStreamFromStreamUsecase,
    create_new_stream_from_stream: Mock,
    save_stream: Mock,
) -> None:
    command = CreateNewStreamCommand(
        project_id=uuid4(),
        stream_name="TEST_STREAM_FAILURE",
        fields=[
            CreateNewStreamCommand.StreamField(name="field_test", type="STRING"),
            CreateNewStreamCommand.StreamField(
                name="another_field_test", type="STRING"
            ),
        ],
        source_name="TEST_STREAM",
        source_type=SourceType.STREAM,
    )
    failure = Failure(FailureDetails(reason="TEST_SAVE_STREAM_FAILS"))
    create_new_stream_from_stream.return_value = Success(command)
    save_stream.return_value = failure

    actual = create_new_stream_from_stream_usecase(command)

    create_new_stream_from_stream.assert_called_with(command)
    save_stream.assert_called_with(command)
    assert isinstance(actual, Result.failure_type)
    assert isinstance(actual.failure(), BusinessFailureDetails)
    assert "NON_BUSINESS_RULE_CAUSE" == actual.failure().reason
    assert failure.failure() == actual.failure().failure_due
