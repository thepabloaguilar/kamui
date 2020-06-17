from unittest.mock import Mock

import pytest
from returns.result import Success, Result, Failure

from kamui.core.entity.topic import TopicNames
from kamui.core.use_case.failure import FailureDetails, BusinessFailureDetails
from kamui.core.use_case.topic.get_available_topic_names import (
    GetTopicNames,
    GetAvailableTopicNamesUseCase,
)


@pytest.fixture(scope="function")
def get_topic_names() -> Mock:
    return Mock(spec=GetTopicNames)


@pytest.fixture(scope="function")
def get_available_topic_names_usecase(
    get_topic_names: Mock,
) -> GetAvailableTopicNamesUseCase:
    return GetAvailableTopicNamesUseCase(get_topic_names)


def test_should_return_an_empty_list_when_no_topic_names_was_returned(
    get_available_topic_names_usecase: GetAvailableTopicNamesUseCase,
    get_topic_names: Mock,
) -> None:
    topic_names = TopicNames([])
    get_topic_names.return_value = Success(topic_names)

    actual = get_available_topic_names_usecase()

    get_topic_names.assert_called_once()
    assert isinstance(actual, Result.success_type)
    assert 0 == len(actual.unwrap())


def test_should_return_an_empty_list_when_no_topic_names_are_valid(
    get_available_topic_names_usecase: GetAvailableTopicNamesUseCase,
    get_topic_names: Mock,
) -> None:
    topic_names = TopicNames(["_firstTopic", "__secondTopic"])
    get_topic_names.return_value = Success(topic_names)

    actual = get_available_topic_names_usecase()

    get_topic_names.assert_called_once()
    assert isinstance(actual, Result.success_type)
    assert 0 == len(actual.unwrap())


def test_should_return_a_list_with_one_item_when_one_topic_name_is_valid(
    get_available_topic_names_usecase: GetAvailableTopicNamesUseCase,
    get_topic_names: Mock,
) -> None:
    topic_names = TopicNames(["availableTopic", "_firstTopic", "__secondTopic"])
    get_topic_names.return_value = Success(topic_names)

    actual = get_available_topic_names_usecase()

    get_topic_names.assert_called_once()
    assert isinstance(actual, Result.success_type)
    assert 1 == len(actual.unwrap())
    assert ["availableTopic"] == actual.unwrap()


def test_should_return_a_list_with_two_items_when_two_topic_name_is_valid(
    get_available_topic_names_usecase: GetAvailableTopicNamesUseCase,
    get_topic_names: Mock,
) -> None:
    topic_names = TopicNames(
        ["availableTopic", "_firstTopic", "__secondTopic", "anotherAvailableTopic_"]
    )
    get_topic_names.return_value = Success(topic_names)

    actual = get_available_topic_names_usecase()

    get_topic_names.assert_called_once()
    assert isinstance(actual, Result.success_type)
    assert 2 == len(actual.unwrap())
    assert ["availableTopic", "anotherAvailableTopic_"] == actual.unwrap()


def test_should_return_failure_when_an_error_is_returned_from_get_topic_names(
    get_available_topic_names_usecase: GetAvailableTopicNamesUseCase,
    get_topic_names: Mock,
) -> None:
    failure = Failure(FailureDetails(reason="This is a test failure"))
    get_topic_names.return_value = failure

    actual = get_available_topic_names_usecase()

    assert isinstance(actual, Result.failure_type)
    assert isinstance(actual.failure(), BusinessFailureDetails)
    assert "NON_BUSINESS_RULE_CAUSE" == actual.failure().reason
    assert failure.failure() == actual.failure().failure_due
