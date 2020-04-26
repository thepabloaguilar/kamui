from unittest.mock import Mock

import pytest
from returns.result import Success, Failure, Result

from kamui.core.entity.topic_schema import (
    TopicSchemaVersions,
    TopicSchema,
    TopicSchemaField,
)
from kamui.core.usecase.failure import FailureDetails, BusinessFailureDetails
from kamui.core.usecase.topic.get_topic_schema import (
    GetTopicSchema,
    GetTopicSchemaVersions,
    GetTopicSchemaUsecase,
)


@pytest.fixture(scope="function")
def get_topic_schema() -> Mock:
    return Mock(spec=GetTopicSchema)


@pytest.fixture(scope="function")
def get_topic_schema_versions() -> Mock:
    return Mock(spec=GetTopicSchemaVersions)


@pytest.fixture(scope="function")
def get_topic_schema_usecase(
    get_topic_schema: Mock, get_topic_schema_versions: Mock
) -> GetTopicSchemaUsecase:
    return GetTopicSchemaUsecase(get_topic_schema, get_topic_schema_versions)


def test_should_return_correctly_topic_schema(
    get_topic_schema_usecase: GetTopicSchemaUsecase,
    get_topic_schema_versions: Mock,
    get_topic_schema: Mock,
) -> None:
    topic_name = "TopicName"
    topic_schema = TopicSchema(
        type="some_type",
        name="TopicName",
        namespace="test_namespace",
        fields=[
            TopicSchemaField(name="field_one", type="STRING"),
            TopicSchemaField(name="field_two", type="INTEGER"),
        ],
    )
    get_topic_schema_versions.return_value = Success(TopicSchemaVersions([1, 2]))
    get_topic_schema.return_value = Success(topic_schema)

    actual = get_topic_schema_usecase(topic_name)

    get_topic_schema_versions.assert_called_with(topic_name)
    get_topic_schema.assert_called_with(2, topic_name=topic_name)
    assert isinstance(actual, Result.success_type)
    assert isinstance(actual.unwrap(), TopicSchema)
    assert topic_schema == actual.unwrap()


def test_should_return_failure_when_get_topic_schema_versions_fails(
    get_topic_schema_usecase: GetTopicSchemaUsecase, get_topic_schema_versions: Mock
) -> None:
    topic_name = "TopicName"
    failure = Failure(FailureDetails(reason="get_topic_schema_versions"))
    get_topic_schema_versions.return_value = failure

    actual = get_topic_schema_usecase(topic_name)

    get_topic_schema_versions.assert_called_with(topic_name)
    assert isinstance(actual, Result.failure_type)
    assert isinstance(actual.failure(), BusinessFailureDetails)
    assert "NON_BUSINESS_RULE_CAUSE" == actual.failure().reason
    assert failure.failure() == actual.failure().failure_due


def test_should_return_failure_when_get_topic_schema_fails(
    get_topic_schema_usecase: GetTopicSchemaUsecase,
    get_topic_schema_versions: Mock,
    get_topic_schema: Mock,
) -> None:
    topic_name = "TopicName"
    failure = Failure(FailureDetails(reason="get_topic_schema"))
    get_topic_schema_versions.return_value = Success(TopicSchemaVersions([1]))
    get_topic_schema.return_value = failure

    actual = get_topic_schema_usecase(topic_name)

    get_topic_schema_versions.assert_called_with(topic_name)
    get_topic_schema.assert_called_with(1, topic_name=topic_name)
    assert isinstance(actual, Result.failure_type)
    assert isinstance(actual.failure(), BusinessFailureDetails)
    assert "NON_BUSINESS_RULE_CAUSE" == actual.failure().reason
    assert failure.failure() == actual.failure().failure_due
