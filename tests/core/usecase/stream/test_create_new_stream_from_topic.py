from unittest.mock import Mock
from uuid import uuid4

import pytest
from returns.result import Failure, Result, Success

from kamui.core.entity.stream import Stream
from kamui.core.usecase.failure import FailureDetails, BusinessFailureDetails
from kamui.core.usecase.stream.create_new_stream import (
    CreateStreamFromKafkaTopic,
    SaveStream,
    CreateNewStreamFromTopicUseCase,
    CreateNewStreamCommand,
    SourceType,
)


@pytest.fixture(scope="function")
def create_new_stream_from_kafka_topic() -> Mock:
    return Mock(spec=CreateStreamFromKafkaTopic)


@pytest.fixture(scope="function")
def save_stream() -> Mock:
    return Mock(spec=SaveStream)


@pytest.fixture(scope="function")
def create_new_stream_from_topic_usecase(
    create_new_stream_from_kafka_topic: Mock, save_stream: Mock
) -> CreateNewStreamFromTopicUseCase:
    return CreateNewStreamFromTopicUseCase(
        create_new_stream_from_kafka_topic, save_stream
    )


def test_should_return_stream_entity_correctly(
    create_new_stream_from_topic_usecase: CreateNewStreamFromTopicUseCase,
    create_new_stream_from_kafka_topic: Mock,
    save_stream: Mock,
) -> None:
    project_id = uuid4()
    command = CreateNewStreamCommand(
        project_id=project_id,
        stream_name="test_stream_success",
        fields=[
            CreateNewStreamCommand.StreamField(name="field_one", type="STRING"),
            CreateNewStreamCommand.StreamField(name="field_two", type="INTEGER"),
        ],
        source_name="from_this_test_success_topic",
        source_type=SourceType.TOPIC,
    )
    stream = Stream(
        stream_id=uuid4(),
        name="test_stream_success",
        source_type=SourceType.TOPIC,
        source_name="test_create_stream",
    )
    create_new_stream_from_kafka_topic.return_value = Success(command)
    save_stream.return_value = Success(stream)

    actual = create_new_stream_from_topic_usecase(command)

    create_new_stream_from_kafka_topic.assert_called_with(command)
    save_stream.assert_called_with(command)
    assert isinstance(actual, Result.success_type)
    assert isinstance(actual.unwrap(), Stream)
    assert stream == actual.unwrap()


def test_should_return_failure_when_create_stream_from_kafka_topic_fails(
    create_new_stream_from_topic_usecase: CreateNewStreamFromTopicUseCase,
    create_new_stream_from_kafka_topic: Mock,
) -> None:
    command = CreateNewStreamCommand(
        project_id=uuid4(),
        stream_name="test_stream_failure",
        fields=[CreateNewStreamCommand.StreamField(name="field_test", type="STRING")],
        source_name="from_this_test_topic",
        source_type=SourceType.TOPIC,
    )
    failure = Failure(FailureDetails(reason="create_new_stream_from_kafka_topic"))
    create_new_stream_from_kafka_topic.return_value = failure

    actual = create_new_stream_from_topic_usecase(command)

    create_new_stream_from_kafka_topic.assert_called_with(command)
    assert isinstance(actual, Result.failure_type)
    assert isinstance(actual.failure(), BusinessFailureDetails)
    assert "NON_BUSINESS_RULE_CAUSE" == actual.failure().reason
    assert failure.failure() == actual.failure().failure_due


def test_should_return_failure_when_save_stream_fails(
    create_new_stream_from_topic_usecase: CreateNewStreamFromTopicUseCase,
    create_new_stream_from_kafka_topic: Mock,
    save_stream: Mock,
) -> None:
    command = CreateNewStreamCommand(
        project_id=uuid4(),
        stream_name="test_stream_failure",
        fields=[
            CreateNewStreamCommand.StreamField(name="field_test", type="STRING"),
            CreateNewStreamCommand.StreamField(
                name="another_field_test", type="STRING"
            ),
        ],
        source_name="from_this_test_topic",
        source_type=SourceType.TOPIC,
    )
    failure = Failure(FailureDetails(reason="save_stream"))
    create_new_stream_from_kafka_topic.return_value = Success(command)
    save_stream.return_value = failure

    actual = create_new_stream_from_topic_usecase(command)

    create_new_stream_from_kafka_topic.assert_called_with(command)
    save_stream.assert_called_with(command)
    assert isinstance(actual, Result.failure_type)
    assert isinstance(actual.failure(), BusinessFailureDetails)
    assert "NON_BUSINESS_RULE_CAUSE" == actual.failure().reason
    assert failure.failure() == actual.failure().failure_due
