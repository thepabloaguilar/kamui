from abc import ABC, abstractmethod

from returns.result import Result

from kamui.core.entity.topic import TopicNames
from kamui.core.usecase.failure import BusinessFailureDetails, FailureDetails


class GetTopicNames(ABC):
    @abstractmethod
    def __call__(self) -> Result[TopicNames, FailureDetails]:
        pass


class GetAvailableTopicNamesUseCase:
    def __init__(self, get_topic_names: GetTopicNames) -> None:
        self.__get_topic_names = get_topic_names

    def __call__(self) -> Result[TopicNames, BusinessFailureDetails]:
        return (
            self.__get_topic_names()
            .alt(
                lambda failure: BusinessFailureDetails(
                    failure_message="Was not possible to get Topic Names",
                    reason="NON_BUSINESS_RULE_CAUSE",
                    failure_due=failure,
                )
            )
            .map(self.__filter_topic_names)
        )

    def __filter_topic_names(self, topic_names: TopicNames) -> TopicNames:
        return TopicNames(
            [topic_name for topic_name in topic_names if not topic_name.startswith("_")]
        )
